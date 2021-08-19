from django.urls import path
from . import views

app_name = "clustering"

urlpatterns = [
    path('', views.home, name="home"),
    path('compute/', views.compute, name="compute"),

    
    # path('', views.clustering_create_view, name='clustering'),
    # path('clustering_args/', views.clustering_args_create_view, name='clustering_args'),
    # path('clustering_results/', views.clustering_results_create_view, name='clustering_results'),
]