from django.contrib import admin
from .models import *

class DatasetAdmin(admin.ModelAdmin):
    list_display=['id','name','dataset_path']
    search_fields=['id','name','dataset_path']

class EntryAdmin(admin.ModelAdmin):
    list_display  = ['article_name','articles_nb_pages','articles_nb_text','article_text','articles_lemmes','article_class','article_dataset']
    search_fields = ['article_name','articles_nb_pages','articles_nb_text','article_text','articles_lemmes','article_class','article_dataset']

admin.site.register(DatasetModel,DatasetAdmin)
admin.site.register(DatasetEntry,EntryAdmin)
