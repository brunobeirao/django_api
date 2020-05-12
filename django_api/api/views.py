# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, generics

from .services import ApiService, ChargeService
from .serializers import CallApiSerializer, CallSerializer, ChargeSerializer


class CallProcess(generics.ListCreateAPIView):
    """
    Process a new call and calculate bills
    """
    parser_classes = [JSONParser]

    serializer_class = CallApiSerializer
    http_method_names = ['post']

    def post(self, request):
        CallApiSerializer(data=request.data)
        api = ApiService()
        api.process_call(request.data)
        return Response(request.data, status=status.HTTP_201_CREATED)


class Call(APIView):
    """
    Return Call by Phone
    """
    @staticmethod
    def get(request, telephone_number, year, month):
        api = ApiService(request.data)
        call = api.get_call(telephone_number, year, month)
        return Response(call, status=status.HTTP_200_OK)


class Charge(generics.ListCreateAPIView):
    serializer_class = ChargeSerializer
    http_method_names = ['post', 'get', 'put']

    def post(self, request):
        """
        Create a new Charge
        """
        ChargeSerializer(data=request.data)
        service = ChargeService(request.data)
        service.save_charge()
        return Response(request.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Get active Charge
        """
        service = ChargeService(request.data)
        charge = service.get_charge_activated()
        serializer = self.serializer_class(charge, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update Charge value
        """
        ChargeSerializer(data=request.data)
        service = ChargeService(request.data)
        service.update_charge()
        return Response(request.data, status=status.HTTP_200_OK)
