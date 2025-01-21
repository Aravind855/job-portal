from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/admin/', register_admin, name='register_admin'),
    path('register/user/', register_user, name='register_user'),
    path('login/admin/', login_admin, name='login_admin'),
    path('login/user/', login_user, name='login_user'),
    path("postjobs", post_job, name="post_job"),
    # path('user/<str:text_id>/', user, name='user'),
    path('jobs/', get_jobs, name='get_jobs'),
    path('fetchjobs', fetch_jobs, name='fetch_jobs'),
]

