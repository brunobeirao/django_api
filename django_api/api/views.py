# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from .services import ApiService
from .serializers import CallsApiSerializer, CallUploadSerializer


import json


class Call(APIView):
    @staticmethod
    def post(request):
        serializer = CallsApiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        api = ApiService(request.data)
        api.calculate_bills()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # @staticmethod
    # def put(request):
    #     api = ApiService(request.data)
    #     serializer = CallsApiSerializer(api)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     api = ApiService(request.data)
    #     serializer = CallsApiSerializer(api)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class DataUploadView(generics.ListCreateAPIView):
    serializer_class = CallUploadSerializer
    http_method_names = ['post']
    # data_dict = request.data
    # def post(self, request, format='json'):
    #     data_dict = request.data
    #     return Response(data_dict, status=status.HTTP_201_CREATED)
