from django.contrib import admin
from .models import userProfile
# Register your models here.
admin.site.register(userProfile)

admin.site.site_header="events scheduler"