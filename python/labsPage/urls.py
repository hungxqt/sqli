from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('setup-db/', views.setup_db_view, name='setup_db'),
    path('view-users/', views.view_users, name='view_users'),
    path('view-emails/', views.view_emails, name='view_emails'),
    path('lab/error-based/', views.lab_error_based, name='lab_error_based'),
    path('reset-db/', views.reset_db_view, name='reset_db'),
]
