from django.urls import path
from . import views

app_name = "manage_data"

urlpatterns = [
    path('enter_data/', views.dataset_create_view, name='enter_data'),
    path('explore/', views.dataset_explore_view, name='explore_data'),
]