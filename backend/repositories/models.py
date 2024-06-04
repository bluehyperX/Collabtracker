import shutil
from django.db import models
import os
from employees.models import Employee

# Create your models here.
class Repository(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    URL = models.CharField(max_length = 255, blank = False)
    
    class Meta:
        verbose_name_plural = 'Repositories'

    def delete_repo(self):
        repo_path = f"../gitrepos/{self.name}"
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        print(os.path.exists(repo_path))

    def delete(self, *args, **kwargs):
        self.delete_repo()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if Repository.objects.filter(URL=self.URL).exists() or Repository.objects.filter(name=self.name).exists():
            old_obj = Repository.objects.get(URL=self.URL) if Repository.objects.filter(URL=self.URL).exists() else Repository.objects.get(name=self.name)
            old_obj.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
class Branch(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    repository = models.ForeignKey(Repository, on_delete = models.CASCADE, blank = False)

    def __str__(self):
        return f"Branch Name: {self.name} Repo: {self.repository}"

class File(models.Model):
    name = models.CharField(max_length = 255, blank = False)
    repository = models.ForeignKey(Repository, on_delete = models.CASCADE, blank = False)

    class Meta:
        unique_together = (('name', 'repository'),)

    def __str__(self):
        return f"File Name: {self.name} Repo: {self.repository}"

class Commit(models.Model):
    hash = models.CharField(max_length = 40, primary_key = True, blank = False)
    authors = models.ManyToManyField(Employee, blank = False)
    repository = models.ForeignKey(Repository, on_delete = models.CASCADE, blank = False)
    branch = models.ForeignKey(Branch, on_delete = models.CASCADE, blank = False)
    created = models.DateTimeField(blank = False)    
    files = models.ManyToManyField(File, blank = False)

    def __str__(self):
        return f"Hash: {self.hash} Authors: {self.authors} Repo: {self.repository}"

# class Changes(models.Model):
#     file = models.ForeignKey(File, on_delete = models.CASCADE, blank = False)
#     commit = models.ForeignKey(Commit, on_delete = models.CASCADE, blank = False)
#     additions = models.IntegerField()
#     deletions = models.IntegerField()