from django.contrib import admin

from .models import JobPosition, Candidate

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'description', 'status', 'vacancies']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['position', 'name', 'email', 'phone', 'stage']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

