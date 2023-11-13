from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import asyncio
from .forms import *
from fetch_data.utilities.tools import territory_divider
from fetch_data.utilities.image_db import *
from .serializers import *


# @login_required(login_url='users:login', )
def territory_fetch(request):
    if request.method == 'GET':
        form = SentinelFetchForm(initial={"inference": True})
        return render(request, "fetch_data/SentinelFetch.html", context={'preset_araes': PresetArea.objects.all(),'form': form,'user':request.user})

    elif request.method == 'POST' and 'fetch' in request.POST and request.user.is_authenticated:
        form = SentinelFetchForm(request.POST)  # x_min, x_max, y_min, y_max, zoom, (start, end, n_days_before_date, date) overwrite_repetitious, image_store_path
        if form.is_valid():
            x_min = form.cleaned_data['x_min']
            x_max = form.cleaned_data['x_max']
            y_min = form.cleaned_data['y_min']
            y_max = form.cleaned_data['y_max']
            zoom = int(form.cleaned_data['zoom'])
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            n_days_before_base_date = form.cleaned_data['n_days_before_base_date']
            base_date = form.cleaned_data['base_date']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            x_range = [int(x_min), int(x_max)]
            y_range = [int(y_min), int(y_max)]

            territories = territory_divider(x_range, y_range, piece_size=70)
            # print(territories)
            for territory in territories:
                for sub_territory in territory:
                    x_range = sub_territory[0]
                    y_range = sub_territory[1]
                    print(sub_territory)
                    territory_fetch_inference(x_range, y_range, zoom, start=start_date, end=end_date, n_days_before_base_date=n_days_before_base_date,
                                              base_date=base_date, overwrite_repetitious=overwrite_repetitious, inference=True)
            # print(form.cleaned_data)
            return render(request, "fetch_data/success.html", context={"form_cleaned_data": form.cleaned_data})
        else:
            return render(request, "fetch_data/error.html", context={'errors': form.errors})
    
    elif request.method == 'POST' and 'fetch' in request.POST and request.user.is_authenticated == False:
        message = "Please login first"
        return HttpResponseRedirect(reverse('users:login'))
    
    elif request.method == 'POST' and 'fill_coords' in request.POST:
        form = SentinelFetchForm(request.POST)
        if form.is_valid():
            preset_area_id = form.cleaned_data['preset_area']
            preset_area = PresetArea.objects.get(tag=preset_area_id)

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            base_date = form.cleaned_data['base_date']
            n_days_before_base_date = form.cleaned_data['n_days_before_base_date']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            form = SentinelFetchForm(initial={"x_min": preset_area.x_min, "x_max": preset_area.x_max, "y_min": preset_area.y_min,
                                              "y_max": preset_area.y_max,"zoom": preset_area.zoom, "start_date": start_date, "end_date": end_date,
                                              "base_date": base_date, "n_days_before_base_date": n_days_before_base_date,
                                              "overwrite_repetitious": overwrite_repetitious, "preset_area": preset_area_id
                                               })
            return render(request, "fetch_data/SentinelFetch.html", {'form': form, 'user':request.user})




def test(request):
    if request.method == 'GET':
        form = SentinelFetchForm(initial={"x_min": 21390, "x_max": 21400, "y_min": 14030, "y_max": 14035, "zoom": 15, "image_store_path": r"D:\SatteliteImages_db"})
        return render(request, "fetch_data/test.html", context={'preset_araes': PresetArea.objects.all(),'form': form,'user':request.user})
    


class territory_fetch_APIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        territory_serializer = TerritorySerializer(data=request.data)
        print(type(territory_serializer))
        print(territory_serializer)
        print("111")
        print("request.data['preset_area']:", request.data['preset_area'])
        if territory_serializer.is_valid():
            if request.data['preset_area'] != None:
                preset_area_obj = PresetArea.objects.get(tag=request.data['preset_area'])
                # preset_area_obj = request.data['preset_area']
                x_min, x_max, y_min, y_max, zoom = preset_area_obj.x_min, preset_area_obj.x_max, preset_area_obj.y_min, preset_area_obj.y_max, preset_area_obj.zoom
            else:
                x_min = request.data.get('x_min', None)
                x_max = request.data.get('x_max', None)
                y_min = request.data.get('y_min', None)
                y_max = request.data.get('y_max', None)
                zoom = int(request.data.get('zoom', None))
            start_date = request.data.get('start_date', None)
            end_date = request.data.get('end_date', None)
            n_days_before_base_date = request.data.get('n_days_before_base_date', None)
            base_date = request.data.get('base_date', None)
            overwrite_repetitious = request.data.get('overwrite_repetitious', None)
            overwrite_repetitious = True if overwrite_repetitious in ["True", "true", "1", True] else False
            x_range = [int(x_min), int(x_max)]
            y_range = [int(y_min), int(y_max)]

            time_interpreted = start_end_time_interpreter(start=start_date, end=end_date, n_days_before_base_date=n_days_before_base_date, base_date=base_date,
                                                        return_formatted_only=False)
            start_date, end_date = time_interpreted[0][0], time_interpreted[1][0]

            territory_fetch_inference(x_range, y_range, zoom, start=start_date, end=end_date, overwrite_repetitious=overwrite_repetitious, )

            request_parameters = {"x_min": x_min, "y_min": y_min, "y_max": y_max, "zoom": zoom, "start_date": start_date, "end_date": end_date,
                                "overwrite_repetitious": overwrite_repetitious}

            return Response(data={"message": "Images stored successfully",
                         "request_parameters": request_parameters
                         }, status=200)
        error_messages = territory_serializer.errors
        return Response(data={"message": error_messages}, status=400)