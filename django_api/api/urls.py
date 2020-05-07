from django.conf.urls import url
from django_api.api.views import CallProcess, Charge, Call

urlpatterns = [
    url(r'^process', CallProcess.as_view(), name='post-process'),
    url(r'^call/(?P<telephone_number>[0-9]{11})/$',
        Call.as_view(), kwargs={'year': None, 'month': None}, name='get-call'),
    url(r'^call/(?P<telephone_number>[0-9]{11})/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        Call.as_view(), name='get-call'),
    url(r'^charge', Charge.as_view(), name='charge'),
]
