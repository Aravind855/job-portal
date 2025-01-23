from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/admin/', register_admin, name='register_admin'),
    path('register/user/', register_user, name='register_user'),
    path('login/admin/', login_admin, name='login_admin'),
    path('login/user/', login_user, name='login_user'),
    path("postjobs/", post_job, name="post_job"),
    path('jobs/', get_jobs, name='get_jobs'),
    path('fetchjobs/', fetch_jobs, name='fetch_jobs'),
    path('company/<str:company_id>/', get_company_details, name='get_company_details'),
    path('company/<str:company_id>/update/', update_company_details, name='update_company_details'),
    path('apply-job/', apply_job, name='apply_job'),
    path('user-applications/', user_applications, name='user_applications'),
    path('job-applicants/<str:job_id>/', job_applicants, name='job_applicants'),
    path('update-application-status/<str:application_id>/', update_application_status, name='update_application_status'),
]

