from django.urls import path
from jobapp.views import *
from .views import jobs_by_category


urlpatterns = [
    path('', index, name='index'),
    path('jobs/',jobs,name='jobs'),
    path('companies/',companies, name='companies'),
    path('services/',services,name='services'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('add_job/', add_job, name='add_job'),
    
    path('job_delete/<int:id>/', job_delete, name='job_delete'),
    path('job/<int:id>/view/', view_job, name='view_job'),
    path('edit-job/<int:job_id>/', job_edit, name='job_edit'), 
    path('job/<int:id>/user_view/', user_view_job, name='user_view_job'), 
    path('view_employee/<int:id>/', view_employee, name='view_employee'),
    path('delete_employee/<int:id>/', delete_employee, name='delete_employee'),
    path('job/<int:job_id>/apply/', apply_job, name='apply_job'),
    
    
    path('view_applications/', view_applications, name='view_applications'),
    path('view_applications/<int:application_id>/', view_application_detail, name='view_application_detail'), 
    path('job-search/', job_search, name='job_search'),
    path('job/<int:job_id>/', viewjob, name='job_detail_1'),
    path('jobs/category/<slug:category>/', jobs_by_category, name='jobs_by_category'),
    path('job/<int:job_id>/', viewjob, name='viewjob'),
    
    
    ]   
    