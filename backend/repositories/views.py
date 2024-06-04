from collections import defaultdict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.utils import timezone

from employees.models import Employee
from .models import Branch, Commit, Repository
from django.db.models import Count, Max, Avg

# Create your views here.
@api_view(["GET"])
def most_active_repos(request):
    most_active_repositories = Repository.objects.annotate(
        total_commits=Count('commit'),
        last_commit=Max("commit__created")
    ).order_by('-total_commits')[:3]

    data = [{'repository_name': repo.name, 'total_commits': repo.total_commits, 'last_commit': repo.last_commit} for repo in most_active_repositories]

    return Response(data=data)

@api_view(["GET"])
def least_active_repos(request):
    least_active_repositories = Repository.objects.annotate(
        total_commits=Count('commit'),
        last_commit=Max("commit__created")
    ).order_by('total_commits')[:3]

    data = [{'repository_name': repo.name, 'total_commits': repo.total_commits, 'last_commit': repo.last_commit} for repo in least_active_repositories]

    return Response(data=data)

@api_view(["GET"])
def repo_data(request):
    # year = request.year
    json_resp = {}
    startDate = datetime(timezone.now().year, 1, 1)
    endDate = datetime(timezone.now().year, 12, 31)

    json_resp['heatmap_dates'] = {'startDate': startDate.strftime('%Y/%m/%d'),'endDate': endDate.strftime('%Y/%m/%d')}
    
    commits = Commit.objects.filter(created__range=(startDate, endDate)
                                    ).values('repository__name', 'created__date'
                                    ).annotate(count=Count('hash'))

    heatmap_data = defaultdict(list)
    facts = defaultdict(list)
    for commit in commits:
        repository_name = commit['repository__name']
        date_str = commit['created__date'].strftime('%Y/%m/%d')
        heatmap_data[repository_name].append({'date': date_str, 'count': commit['count']})
    
    heatmap_data = dict(heatmap_data)

    # Calculate additional data
    repositories = Repository.objects.all()
    branch_data = {}
    user_data = {}
    file_data = {}
    average_commits_per_day = {}
    total_branches = {}
    last_active_branch = {}
    total_users = {}
    last_active_user = {}
    last_commit_datetime = {}
    last_changed_file = {}
    max_changed_files_in_commit = {}
    avg_changed_files_in_commit = {}
    avg_changes_in_file_in_commit = {}

    for repo in repositories:
        # Most active branches
        branches = Commit.objects.filter(repository=repo).values(
            'branch__name'
        ).annotate(
            total_commits=Count('hash'),
            last_commit=Max('created')
        ).order_by('-total_commits')[:3]
        branch_data[repo.name] = list(branches)
        
        # Most active users
        users = Commit.objects.filter(repository=repo).values(
            'authors__name'
        ).annotate(
            total_commits=Count('hash'),
            last_commit=Max('created')
        ).order_by('-total_commits')[:3]
        user_data[repo.name] = list(users)
        
        # Frequently changed files
        files = Commit.objects.filter(repository=repo).values(
            'files__name'
        ).annotate(
            total_commits=Count('hash'),
            last_commit=Max('created')
        ).order_by('-total_commits')[:3]
        file_data[repo.name] = list(files)

        # Average commits per day
        total_commits = Commit.objects.filter(repository=repo, created__range=((timezone.now() - timedelta(days=30)), timezone.now())).count()
        average_commits_per_day[repo.name] = total_commits / 30

         # Total branches
        total_branches[repo.name] = Branch.objects.filter(repository=repo).count()
        
        # Last active branch
        last_active_branch[repo.name] = Commit.objects.filter(repository=repo).values(
            'branch__name'
        ).annotate(
            last_commit=Max('created')
        ).order_by('-last_commit').first()

        # Total users
        total_users[repo.name] = Employee.objects.filter(commit__repository=repo).distinct().count()

        # Last active user
        last_active_user[repo.name] = Commit.objects.filter(repository=repo).values(
            'authors__name'
        ).annotate(
            last_commit=Max('created')
        ).order_by('-last_commit').first()

        # Last commit date and time
        last_commit_datetime[repo.name] = Commit.objects.filter(repository=repo).aggregate(last_commit=Max('created'))['last_commit']

        # Last changed file
        last_changed_file[repo.name] = Commit.objects.filter(repository=repo).values(
            'files__name'
        ).annotate(
            last_commit=Max('created')
        ).order_by('-last_commit').first()

        # Max number of changed files in a commit
        max_changed_files_in_commit[repo.name] = Commit.objects.filter(repository=repo).annotate(
            num_files=Count('files')
        ).aggregate(max_files=Max('num_files'))['max_files']

        # Avg number of changed files in a commit
        avg_changed_files_in_commit[repo.name] = Commit.objects.filter(repository=repo).annotate(
            num_files=Count('files')
        ).aggregate(avg_files=Avg('num_files'))['avg_files']

        # Avg number of changes in a file in a commit
        # Assuming 'changes' field exists in the File model to represent changes made in a commit
        # avg_changes_in_file_in_commit[repo.name] = Commit.objects.filter(repository=repo).annotate(
        #     avg_changes=Avg('files__changes')
        # ).aggregate(avg_changes=Avg('avg_changes'))['avg_changes']


    # Construct the response
    response_data = {
        'heatmap_dates' : {'startDate': startDate.strftime('%Y/%m/%d'),'endDate': endDate.strftime('%Y/%m/%d')},
        'heatmap_data': heatmap_data,
        'branch_data': branch_data,
        'user_data': user_data,
        'file_data': file_data,
        'average_commits_per_day': average_commits_per_day,
        'total_branches': total_branches,
        'last_active_branch': last_active_branch,
        'total_users': total_users,
        'last_active_user': last_active_user,
        'last_commit_datetime': last_commit_datetime,
        'last_changed_file': last_changed_file,
        'max_changed_files_in_commit': max_changed_files_in_commit,
        'avg_changed_files_in_commit': avg_changed_files_in_commit,
        # 'avg_changes_in_file_in_commit': avg_changes_in_file_in_commit
    }

    # json_resp['heatmap_data'] = heatmap_data
    return Response(data=response_data)