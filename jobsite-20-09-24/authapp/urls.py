from django.urls import path
from authapp.views import *
from jobapp.views import *

urlpatterns = [
   

    path('register_company/', register_company, name='register_company'),
    path('login_company/',login_company, name='login_company'), 
    path('user_register/', user_register, name='user_register'),
    path('user_login/',user_login, name='user_login'),
    
    path('mainlogin/',mainlogin,name='mainlogin'),
    
    path('user_dashboard/',user_dashboard, name='user_dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard_admin/', dashboard_admin, name='dashboard_admin'),
    
    path('upload-cv/', upload_cv, name='upload_cv'),
    
    path('edit_employee/<int:id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:id>/', delete_employee, name='delete_employee'),
    path('view_company/<int:id>/', view_company, name='view_company'),
    path('edit_company/<int:id>/', edit_company, name='edit_company'),
    path('delete_company/<int:id>/', delete_company, name='delete_company'),

    path('logout_user/', logout_user, name='logout_user'),
    
    
]

    

