from django.contrib import admin
from .models import Repository
from git import Repo

# Register your models here.
class RepositoryAdmin (admin.ModelAdmin):
    list_display = ("name", "URL")
    list_display_links = ("name", "URL")

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(Repository, RepositoryAdmin)