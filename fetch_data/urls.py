from django.urls import path
from .views import *

app_name = 'fetch_data'

urlpatterns = [
    path('', territory_fetch, name='SentinelFetch'),
    path('bbox-fetch', territory_fetch, name='SentinelFetch-bbox'),
    path('conversions', ConvertView, name='conversions'),
    path('myfetches/last?<int:time_limit>days', MyTasksView, name="myfetches"),
    path('allfetches/last?<int:time_limit>days', AllTasksView, name="allfetches"),
    path('task_result/tasks?<str:task_id>', TaskResult, name="task_result"),
    path('test', test, name='test'),
    path("api-territory_fetch", territory_fetch_APIView.as_view()),
    path('img/task?<str:task_id>/img?<str:image_dir>', ImageGet, name='image_get'),
    path('concat_img/mode?<str:mode>?task?<str:task_id>', ConcatImage, name='image_concat'),
        path('custom_annotation/task?<str:task_id>', CustomAnnotation, name='custom_annotation'),
]