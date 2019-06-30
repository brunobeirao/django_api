# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import ListAPIView
from .services import ApiService


class Start(ListAPIView):

    @staticmethod
    def post(request):
        api = ApiService(request.data)
        return api
