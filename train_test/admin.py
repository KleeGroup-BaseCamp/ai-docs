from django.contrib import admin
from .models import *

class Algoadmin(admin.ModelAdmin):
    list_display=['algo_name','algo_type','dataset']
    search_fields=['algo_name','algo_type','dataset']

admin.site.register(Algo,Algoadmin)
