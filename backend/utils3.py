import git
import logging
import os
import django
from django.utils import timezone
from contextlib import contextmanager

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collabtracker.settings')

# Initialize Django
django.setup()

from repositories.models import Commit, Repository, File, Branch
from employees.models import Employee

date = timezone.now()
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.addHandler(logging.FileHandler(f'utils_{date}.log', 'a'))
print = logger.info

@contextmanager
def open_repo(r):
    repo_path = f"../gitrepos/{r.name}"
    repo = None
    try:
        repo = git.Repo(repo_path)
        print(f"Refreshing Repository - {repo}")
        yield repo
    except git.exc.NoSuchPathError:
        try:
            repo = git.Repo.clone_from(r.URL, repo_path)
            print(f"Created Repository - {repo}")
            for b in repo.branches:
                Branch.objects.create(name=b.name, repository=r)
                print(f"Created branch - {b.name}")
            yield repo
        except Exception as e:
            raise f"Error cloning repository {r.name}: {e}"
    finally:
        if repo:
            repo.close()

def get_commits(r, repo):
    for branch in repo.branches:
        print(f"Processing branch: {branch}")
        for commit in repo.iter_commits(branch):
            print(f"Processing commit: {commit.hexsha}")
            if Commit.objects.filter(hash=commit.hexsha).exists():
                continue
            commit_info = Commit.objects.create(
                hash=commit.hexsha, 
                repository=r, 
                branch=Branch.objects.get(name=branch.name, repository=r), 
                created=commit.committed_datetime
            )
            commit_info.authors.add(Employee.objects.get_or_create(name=commit.author.name)[0])
            for author in commit.co_authors:
                commit_info.authors.add(Employee.objects.get_or_create(name=author.name)[0])
            if commit.parents:
                for diff in commit.diff(commit.parents[0]):
                    try:
                        commit_info.files.add(File.objects.get_or_create(name=diff.a_path, repository=r)[0])
                    except Exception as e:
                        print(f"Error in adding file {diff.a_path}: {e}")
                        continue

def get_branches(r, repo):
    origin = repo.remote(name='origin')
    origin.fetch()
    remote_branches = []

    for ref in repo.references:
        try:
            if isinstance(ref, git.RemoteReference):
                branch = ref.remote_head
                if branch and branch != 'HEAD':
                    remote_branches.append(branch)
        except Exception as e:
            print(f"Error in finding branch {r.name}: {e}")
            continue

    local_branches = [b.name for b in repo.branches]
    local_only_branches = set(local_branches) - set(remote_branches)

    for b in local_only_branches:
        repo.git.branch('-D', b)
        Branch.objects.filter(name=b, repository=r).delete()
        print(f"Deleted local branch - {b}")

    remote_only_branches = set(remote_branches) - set(local_branches)
    for b in remote_only_branches:
        repo.git.checkout(b)
        Branch.objects.create(name=b, repository=r)
        print(f"Created new branch - {b}")

    for b in repo.branches:
        try:
            repo.git.checkout(b)
            origin.pull(b)
            print(f"Updated branch - {b}")
        except Exception as e:
            raise f"Error while updating branch {b}: {e}"
        
    repo.git.checkout('master')

def main():
    
    for r in Repository.objects.all():
        with open_repo(r) as repo:
            try:
                get_branches(r, repo)
                get_commits(r, repo)
            except Exception as e:
                raise f"Error processing repository {r.name}: {e}"

if __name__ == "__main__":
    main()