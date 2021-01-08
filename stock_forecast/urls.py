from django.urls import include, path
from rest_framework import routers
from . import views
from .drf import viewsets

router = routers.DefaultRouter()
# router.register(r'companies-list', viewsets.TaskViewSet, basename='companies-list')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('prediction', views.StockPredictionView.as_view(), name="prediction"),
    # path(r'trained-companies-list', viewsets.CompaniesListView.as_view(), name="trained-companies-list")
]
