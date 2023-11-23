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
from django.contrib import auth
import asyncio, logging, time, datetime
from asgiref.sync import sync_to_async
from celery import shared_task
from .forms import *
from fetch_data.utilities.tools import territory_divider, xyz2bbox_territory, coords_2_xyz_newton, get_current_datetime
from fetch_data.utilities.image_db import *
from .serializers import *


# @shared_task
async def fetch(territories, x_min, x_max, y_min, y_max, zoom, start_date, end_date, task_id, overwrite_repetitious, inference, save_concated):
    n_total_queries = (x_max - x_min + 1) * (y_max - y_min + 1)
    n_queries_done = 0
    for idx, territory in enumerate(territories):
        logging.info(f"Territory {idx} (out of {len(territories)}) began fetching")
        for sub_territory in territory:
            x_range = sub_territory[0]
            y_range = sub_territory[1]
            t1 = time.perf_counter()
            n_queries_done = territory_fetch_inference(x_range, y_range, zoom, start_date=start_date, end_date=end_date, task_id=task_id,
                                    n_queries_done=n_queries_done, n_total_queries=n_total_queries,
                                    overwrite_repetitious=overwrite_repetitious, inference=inference, save_concated=save_concated)
            logging.info(f"{time.perf_counter() - t1} seconds to fetch this territory")

@login_required(login_url='users:login')
async def territory_fetch(request):
    user = await sync_to_async(auth.get_user)(request)    
    if request.method == 'GET':
        form = SentinelFetchForm()
        return render(request, "fetch_data/SentinelFetch.html", context={'preset_araes': PresetArea.objects.all(),'form': form,
                                                                        #  'user':request.user,
                                                                         'user': user,
                                                                         })

    elif request.method == 'POST' and 'fetch' in request.POST and request.user.is_authenticated:
        form = SentinelFetchForm(request.POST)  # x_min, x_max, y_min, y_max, zoom, (start, end, n_days_before_date, date) overwrite_repetitious, image_store_path
        coordinate_type = request.POST.get('coordinate_type')
        coordinate_type = "lonlat" if coordinate_type == None else coordinate_type
        date_type = request.POST.get('date_type')
        save_concated = True if request.POST.get('save_concated') == "True" else False
        if form.is_valid():
            zoom = int(form.cleaned_data['zoom'])
            if coordinate_type == "xy":
                x_min = form.cleaned_data['x_min']
                x_max = form.cleaned_data['x_max']
                y_min = form.cleaned_data['y_min']
                y_max = form.cleaned_data['y_max']
                x_range = [int(x_min), int(x_max)]
                y_range = [int(y_min), int(y_max)]
                lon_min, lat_min, lon_max, lat_max = xyz2bbox_territory(x_range, y_range, zoom)
            elif coordinate_type == "lonlat":
                lon_min = form.cleaned_data['lon_min']
                lon_max = form.cleaned_data['lon_max']
                lat_min = form.cleaned_data['lat_min']
                lat_max = form.cleaned_data['lat_max']
                coords = (lon_min, lat_min, lon_max, lat_max)
                x_range, y_range, _ = coords_2_xyz_newton(coords, zoom)
                (x_min, x_max), (y_min, y_max) = x_range, y_range
            if date_type == 'start_end':
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
            elif date_type == 'days_before':
                n_days_before_base_date = form.cleaned_data['n_days_before_base_date']
                base_date = form.cleaned_data['base_date']
                date_data = start_end_time_interpreter(n_days_before_base_date=n_days_before_base_date, base_date=base_date)
                start_date = date_data['start_date']
                end_date = date_data['end_date']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            inference = form.cleaned_data['inference']
            territories = territory_divider(x_range, y_range, piece_size=70)
            logging.info(f"\nterritories:\n{territories}\n")

            # QueuedTask lines
            task_id = f"user.username-[{lon_min},{lat_min},{lon_max},{lat_max}]-({start_date}_{end_date})-q_{get_current_datetime()}"
            task_type = "fetch_infer" if inference else "fetch"
            try:
                area_tag = PresetArea.objects.get(lon_min=lon_min, lat_min=lat_min, lon_max=lon_max, lat_max=lat_max)
            except PresetArea.DoesNotExist:
                area_tag = None
            task = QueuedTasks.objects.create(task_id=task_id, task_type=task_type, task_status="fetching", fetch_progress=0, 
                                       lon_min=lon_min, lat_min=lat_min, lon_max=lon_max, lat_max=lat_max, 
                                       zoom=zoom, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max,
                                       time_from=start_date, time_to=end_date, user_queued=request.user,)
            if area_tag != None:
                task.area_tag=area_tag
                task.save()
            ### End QueuedTask lines
            await fetch(territories, x_min, x_max, y_min, y_max, zoom, start_date, end_date, task_id,
            overwrite_repetitious, inference, save_concated)

            # loop = asyncio.get_event_loop()
            # task = loop.create_task(fetch(territories, x_min, x_max, y_min, y_max, zoom, start_date, end_date, task_id, overwrite_repetitious, inference, save_concated))
            # await task
            
            # fetch.delay(territories, x_min, x_max, y_min, y_max, zoom, start_date, end_date, task_id,
                        # overwrite_repetitious, inference, save_concated)
            
            # await fetch(territories, x_min, x_max, y_min, y_max, zoom, start_date, end_date, task_id,
            # overwrite_repetitious, inference, save_concated)

            # n_total_queries = (x_max - x_min + 1) * (y_max - y_min + 1)
            # n_queries_done = 0
            # for idx, territory in enumerate(territories):
            #     print(territories)
            #     logging.info(f"Territory {idx} (out of {len(territories)}) began fetching")
            #     for sub_territory in territory:
            #         x_range = sub_territory[0]
            #         y_range = sub_territory[1]
            #         t1 = time.perf_counter()
            #         n_queries_done = territory_fetch_inference(x_range, y_range, zoom, start_date=start_date, end_date=end_date, task_id=task_id,
            #                                 n_queries_done=n_queries_done, n_total_queries=n_total_queries,
            #                                 overwrite_repetitious=overwrite_repetitious, inference=inference, save_concated=save_concated)
            #         logging.info(f"{time.perf_counter() - t1} seconds to fetch this territory")        
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
            zoom = int(form.cleaned_data['zoom'])
            preset_area = PresetArea.objects.get(tag=preset_area_id)
            coords = [preset_area.lon_min, preset_area.lat_min, preset_area.lon_max, preset_area.lat_max]
            lon_min, lat_min, lon_max, lat_max = coords
            x_range, y_range, _ = coords_2_xyz_newton(coords, zoom)
            (x_min, x_max), (y_min, y_max) = x_range, y_range

            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            base_date = form.cleaned_data['base_date']
            n_days_before_base_date = form.cleaned_data['n_days_before_base_date']
            inference = form.cleaned_data['inference']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            save_concated = True if request.POST.get('save_concated') == "True" else False
            form = SentinelFetchForm(initial={"x_min": x_min, "x_max": x_max, "y_min": y_min,
                                              "y_max": y_max,"zoom": zoom, "lon_min": lon_min,
                                              "lon_max": lon_max, "lat_min": lat_min,
                                              "lat_max": lat_max, "start_date": start_date, "end_date": end_date,
                                              "base_date": base_date, "n_days_before_base_date": n_days_before_base_date,
                                              "overwrite_repetitious": overwrite_repetitious, "preset_area": preset_area_id,
                                              'inference': inference,
                                               })
            return render(request, "fetch_data/SentinelFetch.html", {'form': form, 'user':request.user})
        
    elif request.method == 'POST' and 'last_10_days' in request.POST:
        form = SentinelFetchForm(request.POST)
        logging.info("\n\n\n\Last 10 days form - before validation\n\n\n")
        if form.is_valid():
            logging.info("\n\n\n\Last 10 days form is valid\n\n\n")
            preset_area = form.cleaned_data['preset_area']
            zoom = form.cleaned_data['zoom']
            lon_min = form.cleaned_data['lon_min']
            lon_max = form.cleaned_data['lon_max']
            lat_min = form.cleaned_data['lat_min']
            lat_max = form.cleaned_data['lat_max']
            x_min = form.cleaned_data['x_min']
            x_max = form.cleaned_data['x_max']
            y_min = form.cleaned_data['y_min']
            y_max = form.cleaned_data['y_max']

            end_date = datetime.datetime.now().date()
            start_date = end_date - datetime.timedelta(days=10)
            base_date = end_date
            n_days_before_base_date = 10
            inference = form.cleaned_data['inference']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            save_concated = True if request.POST.get('save_concated') == "True" else False
            form = SentinelFetchForm(initial={"x_min": x_min, "x_max": x_max, "y_min": y_min,
                                                "y_max": y_max,"zoom": zoom, "lon_min": lon_min,
                                                "lon_max": lon_max, "lat_min": lat_min,
                                                "lat_max": lat_max, "start_date": start_date, "end_date": end_date,
                                                "base_date": base_date, "n_days_before_base_date": n_days_before_base_date,
                                                "overwrite_repetitious": overwrite_repetitious, "preset_area": preset_area,
                                                'inference': inference,
                                                })
            return render(request, "fetch_data/SentinelFetch.html", {'form': form, 'user':request.user})
        logging.info("\n\n\n\Last 10 days form is not valid\n\n\n")


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
    

@login_required(login_url='users:login')
def ConvertView(request):
    if request.method == 'GET':
        logging.info("GET 1")
        form_2xy = Convert2xyForm()
        form_2lonlat = Convert2lonlatForm()
        return render(request, "fetch_data/Conversions.html", context={'form_2xy': form_2xy,
        "form_2lonlat": form_2lonlat,'user':request.user})

    elif request.method == 'POST' and 'convert_2lonlat' in request.POST and request.user.is_authenticated:
        form_2lonlat = Convert2lonlatForm(request.POST)
        form_2xy = Convert2xyForm(request.POST)
        decimal_round = int(request.POST.get('decimal_round')) if request.POST.get('decimal_round')!=None else 6
        if form_2lonlat.is_valid():
            zoom_2lonlat = form_2lonlat.cleaned_data['zoom_2lonlat']
            x_min_2lonlat = form_2lonlat.cleaned_data['x_min_2lonlat']
            x_max_2lonlat = form_2lonlat.cleaned_data['x_max_2lonlat']
            y_min_2lonlat = form_2lonlat.cleaned_data['y_min_2lonlat']
            y_max_2lonlat = form_2lonlat.cleaned_data['y_max_2lonlat']

            x_range_2lonlat = (x_min_2lonlat, x_max_2lonlat)
            y_range_2lonlat = (y_min_2lonlat, y_max_2lonlat)
            lon_min_2lonlat, lat_min_2lonlat, lon_max_2lonlat, lat_max_2lonlat = xyz2bbox_territory(x_range_2lonlat, y_range_2lonlat, zoom_2lonlat)
            lon_min_2lonlat, lat_min_2lonlat, lon_max_2lonlat, lat_max_2lonlat = list(map(lambda x: round(x, decimal_round), (lon_min_2lonlat, lat_min_2lonlat, lon_max_2lonlat, lat_max_2lonlat)))
            convert_2lonlat_res = {'lon_min_2lonlat': lon_min_2lonlat, 'lat_min_2lonlat': lat_min_2lonlat, 'lon_max_2lonlat': lon_max_2lonlat, 'lat_max_2lonlat': lat_max_2lonlat}

            return render(request, "fetch_data/Conversions.html", context={'form_2xy': form_2xy,
            "form_2lonlat": form_2lonlat, 'convert_2lonlat_res': convert_2lonlat_res ,'user':request.user})


    elif request.method == 'POST' and 'convert_2xy' in request.POST and request.user.is_authenticated:
        logging.info("before form_2xy validation")
        print("before form_2xy validation")
        form_2xy = Convert2xyForm(request.POST)
        form_2lonlat = Convert2lonlatForm(request.POST)
        logging.info("before form_2xy validation")
        if form_2xy.is_valid():
            zoom_2xy = form_2xy.cleaned_data['zoom_2xy']
            lon_min_2xy = form_2xy.cleaned_data['lon_min_2xy']
            lon_max_2xy = form_2xy.cleaned_data['lon_max_2xy']
            lat_min_2xy = form_2xy.cleaned_data['lat_min_2xy']
            lat_max_2xy = form_2xy.cleaned_data['lat_max_2xy']

            coords_2xy = (lon_min_2xy, lat_min_2xy, lon_max_2xy, lat_max_2xy)
            (x_min_2xy, x_max_2xy), (y_min_2xy, y_max_2xy), zoom_2xy = coords_2_xyz_newton(coords_2xy, zoom_2xy)
            convert_2xy_res = {"x_min_2xy": x_min_2xy, "x_max_2xy": x_max_2xy, 'y_min_2xy': y_min_2xy, 'y_max_2xy': y_max_2xy, 'zoom_2xy': zoom_2xy}
            print("convert_2xy_res:", convert_2xy_res)

            return render(request, "fetch_data/Conversions.html", context={'form_2xy': form_2xy,
            "form_2lonlat": form_2lonlat, 'convert_2xy_res': convert_2xy_res, 'user':request.user})


@login_required(login_url='users:login')
def MyTasksView(request):
    if request.method=="GET" and request.user.is_authenticated:
        user = request.user
        tasks =  QueuedTasks.objects.filter(user_queued=user).order_by('-time_queued')
        return render(request, "fetch_data/MyTasks.html", context={'tasks': tasks, 'user':user})