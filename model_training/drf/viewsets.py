from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
import json
from django.conf import settings
from model_training.models import CompanyModelDtls




class CompaniesListView(APIView):
    """
    A simple APIView for listing or retrieving users.
    """
    def get(self, request):
        query_params= self.request.query_params
        is_trained = query_params.get('is_trained')
        companyQuerySet = CompanyModelDtls.objects.all()
        if is_trained and is_trained == "1":
            values= ("symbol", "company_name", "country", "trained_on")
            data = list(companyQuerySet.filter(is_trained=True).values(*values))
        else:
            values = ("symbol", "company_name", "country", "trained_on")
            data = list(companyQuerySet.values(*values))
        return Response(data)