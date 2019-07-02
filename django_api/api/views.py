# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ApiService
from .serializers import CallsApiSerializer


class Start(APIView):

    @staticmethod
    def post(request):
        api = ApiService(request.data)
        serializer = CallsApiSerializer(api)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
0