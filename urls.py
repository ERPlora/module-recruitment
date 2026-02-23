from django.urls import path
from . import views

app_name = 'recruitment'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('positions/', views.positions, name='positions'),
    path('candidates/', views.candidates, name='candidates'),
    path('settings/', views.settings, name='settings'),
]
