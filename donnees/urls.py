from django.urls import path,include
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "donnees"

urlpatterns = [
    path('dataset_models/', views.dataset_modelViewSet.as_view()),
    path('dataset_entries/', views.dataset_entryViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)