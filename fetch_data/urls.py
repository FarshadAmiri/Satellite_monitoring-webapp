from django.urls import path
from .views import *

app_name = 'fetch_data'

urlpatterns = [
    path('', territory_fetch, name='SentinelFetch'),
    path('bbox-fetch', territory_fetch, name='SentinelFetch-bbox'),
    path('conversions', ConvertView, name='conversions'),
    path('myfetches', MyTasksView, name="myfetches"),
    path('allfetches', AllTasksView, name="allfetches"),
    path('task_result/taski?<str:task_id>', TaskResult, name="task_result"),
    path('test', test, name='test'),
    path("api-territory_fetch", territory_fetch_APIView.as_view()),
]