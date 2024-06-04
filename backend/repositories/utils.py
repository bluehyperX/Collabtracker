import git
from repositories.models import Commit, Repository, File, Branch
from employees.models import Employee

def get_commits(r, repo):
    for branch in repo.branches:
        for commit in repo.iter_commits(branch):
            if Commit.objects.filter(hash=commit.hexsha).exists():
                continue
            commit_info = Commit.objects.create(hash = commit.hexsha, repository = r, branch = Branch.objects.get(name=branch.name, repository=r), created = commit.committed_datetime)
            commit_info.authors.add(Employee.objects.get_or_create(name=commit.author)[0])
            for author in commit.co_authors:
                commit_info.authors.add(Employee.objects.get_or_create(name=author)[0])
            try:
                for diff in commit.diff(commit.parents[0]):
                    file = File.objects.get_or_create(name=diff.a_path)[0]
                    commit_info.files.add(file)
            except:
                pass
            print('done!')

def get_branches(r, repo):
    origin = repo.remote(name='origin')
    origin.fetch()
    remote_branches=[]
    for ref in repo.references:
        try:
            if ref.remote_head:
                branch = ref.remote_head
                if (branch!='HEAD'):
                    remote_branches.append(branch)
        except:
            continue 
    local_branches=[b.name for b in repo.branches]
    local_only_branches = set(local_branches) - set(remote_branches)
    for b in local_only_branches:
        repo.git.branch('-D',b)
        Branch.objects.filter(name=b, repository=r).delete()
        print(f"Deleted branch - {b}")
    remote_only_branches = set(remote_branches) - set(local_branches)
    for b in remote_only_branches:
        repo.git.checkout(b)
        Branch.objects.create(name=b, repository=r)
        print(f"Created branch - {b}")

for r in Repository.objects.all():
    try:
        repo = git.Repo(f"../gitrepos/{r.name}")
    except:
        repo = git.Repo.clone_from(r.URL, f"../gitrepos/{r.name}")
    get_branches(r, repo)
    get_commits(r, repo)
    repo.close()