# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .services import ApiService
from .serializers import CallsApiSerializer, CallsSerializer, ChargesSerializer
import json


class CallProcess(generics.ListCreateAPIView):
    serializer_class = CallsApiSerializer
    http_method_names = ['post']

    def post(self, request):
        CallsApiSerializer(data=request.data['data'])
        data = json.loads(request.data['data'])
        api = ApiService(data)
        api.process_calls()
        return Response(data, status=status.HTTP_201_CREATED)
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


class Charge(generics.ListCreateAPIView):
    serializer_class = ChargesSerializer
    http_method_names = ['post']
    
    def post(self, request):
        serializer = ChargesSerializer(data=request.data)
        api = ApiService(serializer)
        api.process_calls()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DataUploadView(generics.ListCreateAPIView):
    serializer_class = CallsSerializer
    http_method_names = ['post']

    # data_dict = request.data
    def post(self, request):
        serializer = CallsSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        data = json.loads(request.data['data'])
        api = ApiService(data)
        api.save_start_call()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
