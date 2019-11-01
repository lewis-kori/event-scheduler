from django.contrib import admin
from .models import Event,Reviews,Attendees
# Register your models here.
admin.site.register(Event)
admin.site.register(Reviews)
admin.site.register(Attendees)
