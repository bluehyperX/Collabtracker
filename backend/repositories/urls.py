from django.urls import path
from . import views

urlpatterns = [
    path('repo_data', views.repo_data, name='repo_data'),
    path('most_active_repos', views.most_active_repos, name='most_active_repos'),
    path('least_active_repos', views.least_active_repos, name='least_active_repos')
]