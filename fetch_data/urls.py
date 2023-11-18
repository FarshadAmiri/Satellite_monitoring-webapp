from django.urls import path
from .views import *

app_name = 'fetch_data'

urlpatterns = [
    path('', territory_fetch, name='SentinelFetch'),
    path('bbox-fetch', territory_fetch, name='SentinelFetch-bbox'),
    path('conversions', ConvertView, name='conversions'),
    path('test', test, name='test'),
    path("api-territory_fetch", territory_fetch_APIView.as_view())
]