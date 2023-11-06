from django.urls import path
from .views import *

app_name = 'fetch_data'

urlpatterns = [
    path('', territory_fetch, name='SentinelFetch'),
    
]