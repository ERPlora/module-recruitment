from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # JobPosition
    path('job_positions/', views.job_positions_list, name='job_positions_list'),
    path('job_positions/add/', views.job_position_add, name='job_position_add'),
    path('job_positions/<uuid:pk>/edit/', views.job_position_edit, name='job_position_edit'),
    path('job_positions/<uuid:pk>/delete/', views.job_position_delete, name='job_position_delete'),
    path('job_positions/<uuid:pk>/toggle/', views.job_position_toggle_status, name='job_position_toggle_status'),
    path('job_positions/bulk/', views.job_positions_bulk_action, name='job_positions_bulk_action'),

    # Candidate
    path('candidates/', views.candidates_list, name='candidates_list'),
    path('candidates/add/', views.candidate_add, name='candidate_add'),
    path('candidates/<uuid:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('candidates/<uuid:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    path('candidates/bulk/', views.candidates_bulk_action, name='candidates_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
