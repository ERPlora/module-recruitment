from django.contrib import admin

from .models import JobPosition, Candidate

@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'status', 'vacancies', 'created_at']
    search_fields = ['title', 'department', 'description', 'status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['position', 'name', 'email', 'phone', 'stage', 'created_at']
    search_fields = ['name', 'email', 'phone', 'stage']
    readonly_fields = ['created_at', 'updated_at']

