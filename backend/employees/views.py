from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from repositories.models import Commit
from django.db.models import Count, Max, Avg
from collections import defaultdict

@api_view(["GET"])
def user_data(request):
    json_resp = {}
    startDate = datetime(timezone.now().year, 1, 1)
    endDate = datetime(timezone.now().year, 12, 31)

    json_resp['heatmap_dates'] = {'startDate': startDate.strftime('%Y/%m/%d'),'endDate': endDate.strftime('%Y/%m/%d')}
    
    commits = Commit.objects.filter(created__range=(startDate, endDate)
                                    ).values('authors__name', 'created__date'
                                    ).annotate(count=Count('hash'))

    heatmap_data = defaultdict(list)
    for commit in commits:
        authors_name = commit['authors__name']
        date_str = commit['created__date'].strftime('%Y/%m/%d')
        heatmap_data[authors_name].append({'date': date_str, 'count': commit['count']})
    
    heatmap_data = dict(heatmap_data)
    json_resp['heatmap_data'] = heatmap_data

    top_repos_data = defaultdict(list)
    productive_days_data = defaultdict(list)

    # Calculate top 3 repositories and most productive days for each user
    for author_name in heatmap_data.keys():
        author_commits = Commit.objects.filter(authors__name=author_name, created__range=(startDate, endDate))
        
        # Top 3 repositories
        top_repos = author_commits.values('repository__name').annotate(
            total_commits=Count('hash'),
            last_commit=Max('created')
        ).order_by('-total_commits')[:3]
        
        top_repos_data[author_name] = [
            {
                'repository_name': repo['repository__name'],
                'total_commits': repo['total_commits'],
                'last_commit': repo['last_commit'].strftime('%Y/%m/%d')
            } for repo in top_repos
        ]

        # Most productive days of the week
        productive_days = author_commits.values('created__week_day').annotate(
            avg_commits=Count('hash')/52.000
        ).order_by('-avg_commits')[:3]
        
        days_of_week = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday', 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
        
        productive_days_data[author_name] = [
            {
                'day': days_of_week[day['created__week_day']],
                'avg_commits': day['avg_commits']
            } for day in productive_days
        ]

    json_resp['top_repositories'] = dict(top_repos_data)
    json_resp['most_productive_days'] = dict(productive_days_data)
    
    return Response(data=json_resp)
