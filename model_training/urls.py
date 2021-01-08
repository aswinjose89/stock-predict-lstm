from django.urls import include, path
from . import views
from .drf import viewsets


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('stock-training', views.StockModelTrainingView.as_view(), name="stock-training"),
    path(r'companies-list', viewsets.CompaniesListView.as_view(), name="companies-list")
]
