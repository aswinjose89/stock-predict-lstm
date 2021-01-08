from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
import json
from django.conf import settings
from stock_forecast.models import Task, tasks
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from model_training.models import CompanyModelDtls

#
# STATUSES= ((1, 'New'))
#
# # class TaskFilter(filters.FilterSet):
# #     class Meta:
# #         model = Task
# #         fields = {'id': ['exact', 'in', 'startswith']}
# class CustomSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         import pdb
#         pdb.set_trace()
#         if request.query_params.get('title_only'):
#             return ['title']
#         return super(CustomSearchFilter, self).get_search_fields(view, request)
#
# class IsOwnerFilterBackend(filters.BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         import pdb
#         pdb.set_trace()
#         return queryset.filter(owner=request.user)
#
# class TaskSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=256)
#     owner = serializers.CharField(max_length=256)
#     status = serializers.ChoiceField(choices=STATUSES, default='New')
#
#     def create(self, validated_data):
#         return Task(id=None, **validated_data)
#
#     def update(self, instance, validated_data):
#         for field, value in validated_data.items():
#             setattr(instance, field, value)
#         return instance
#
#
# class TaskViewSet(viewsets.ViewSet):
#     # Required for the Browsable API renderer to have a nice form.
#     serializer_class = TaskSerializer
#     filter_backends = [IsOwnerFilterBackend]
#     search_fields = ['id', 'name']
#     ordering_fields = '__all__'
#
#     def list(self, request):
#         import pdb
#         pdb.set_trace()
#         serializer = TaskSerializer(
#             instance=tasks.values(), many=True)
#         return Response(serializer.data)

class CompaniesListView(APIView):
    """
    A simple APIView for listing or retrieving users.
    """
    def get(self, request):
        companyQuerySet = CompanyModelDtls.objects.all()
        data = list(companyQuerySet.values("symbol", "company_name", "country"))
        return Response(data)