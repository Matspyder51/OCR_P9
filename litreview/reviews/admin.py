from django.contrib import admin
from .models import Ticket, Request

# Register your models here.
admin.site.register([Ticket, Request])