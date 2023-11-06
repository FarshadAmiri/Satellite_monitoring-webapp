from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from .forms import *
from .utility_image_db import *


# def SentinelFetch(request):
#     if request.method == 'GET':
#         form = SentinelFetchForm()
#         return render(request, "SentinelFetch.html", context={'flights': Flight.objects.all(),'form': form,'user':request.user})
    
#     elif request.method == 'POST':
#         form = SearchFlight(request.POST)
#         if form.is_valid():
#             origin = form.cleaned_data['origin']
#             destination = form.cleaned_data['destination']
#             return HttpResponseRedirect(reverse('flights:search_flight', kwargs={'origin':origin, 'destination':destination}))
#         return render(request, 'Error_page.html', {'message':form.errors['err']})

def territory_fetch(request):
    if request.method == 'GET':
        form = SentinelFetchForm()
        return render(request, "fetch_data/SentinelFetch.html", context={'preset_araes': PresetArea.objects.all(),'form': form,'user':request.user})

    elif request.method == 'POST':
        form = SentinelFetchForm(request.POST)  # x_min, x_max, y_min, y_max, zoom, (start, end, n_days_before_date, date) overwrite_repetitious, image_store_path
        if form.is_valid():
            x_min = form.cleaned_data['x_min']
            x_max = form.cleaned_data['x_max']
            y_min = form.cleaned_data['y_min']
            y_max = form.cleaned_data['y_max']
            zoom = form.cleaned_data['zoom']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            n_days_before_date = form.cleaned_data['n_days_before_date']
            base_date = form.cleaned_data['base_date']
            overwrite_repetitious = form.cleaned_data['overwrite_repetitious']
            image_store_path = form.cleaned_data['image_store_path']
            x_range = [x_min, x_max]
            y_range = [y_min, y_max]
            store_image_territory(x_range, y_range, zoom, start=start_date, end=end_date, n_days_before_date=n_days_before_date, date=base_date,
                                  overwrite_repetitious=overwrite_repetitious, image_store_path=image_store_path)
            

    
    
