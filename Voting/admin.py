from django.contrib import admin

# Register your models here.

from .models import UserVoteStatus,Candidate

@admin.register(UserVoteStatus)
class UserVoteStatusAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'voted_at']
    list_filter = ['user', 'voted_at']

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'User'

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'party', 'position', 'votes']
    list_filter = ['party', 'position']
    readonly_fields=['votes']