# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from .services import ApiService, ChargeService
from .serializers import CallApiSerializer, CallSerializer, ChargeSerializer


class CallProcess(generics.ListCreateAPIView):
    """
    Process a new call and calculate bills
    """
    serializer_class = CallApiSerializer
    http_method_names = ['post']

    def post(self, request):
        for request in request.data:
            CallApiSerializer(data=request)
            api = ApiService(request)
            api.process_calls()
        return Response(request, status=status.HTTP_201_CREATED)


class Call(APIView):
    """
    Return Call by ID
    """
    serializer_class = CallSerializer

    def get(self, request, call_id):
        api = ApiService(request.data)
        call = api.get_call(call_id)
        serializer = self.serializer_class(call, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
