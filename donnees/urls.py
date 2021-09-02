from django.urls import path,include
from rest_framework import routers
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "donnees"


# router = routers.DefaultRouter()
# router.register(r'dataset_model', views.dataset_modelViewSet)
# router.register(r'dataset_entry', views.dataset_entryViewSet)

# # Wire up our API using automatic URL routing.
# # Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]
urlpatterns = [
    path('dataset_models/', views.dataset_modelViewSet.as_view()),
    path('dataset_entries/', views.dataset_entryViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)