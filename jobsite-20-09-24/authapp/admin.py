from django.contrib import admin
from authapp.models import *

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Employee)

