from django.urls import path
from . import views

urlpatterns = [
    path('', views.lab_unified, name='home'),
    path('union/', views.union_lab, name='union'),
    path('reflect/', views.reflect_lab, name='reflect'),
    path('boolean/', views.boolean_lab, name='boolean'),
    path('time/', views.time_lab, name='time'),
    path('setup-db/', views.setup_db_view, name='setup_db'),
    path('view-users/', views.view_users, name='view_users'),
    path('view-emails/', views.view_emails, name='view_emails'),
    path('reset-db/', views.reset_db_view, name='reset_db'),
]
