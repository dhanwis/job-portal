from django.contrib import admin
from jobapp.models import *
# jobapp/admin.py

from django.contrib import admin
from .models import Job, JobApplication


admin.site.register(Job)
admin.site.register(JobApplication)

