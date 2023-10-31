from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from .models import Flight
from .forms import *


def SentinelFetch(request):
    if request.method == 'GET':
        form = SentinelFetchForm()
        return render(request, "SentinelFetch.html", context={'flights': Flight.objects.all(),'form': form,'user':request.user})
    
    elif request.method == 'POST':
        form = SearchFlight(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            return HttpResponseRedirect(reverse('flights:search_flight', kwargs={'origin':origin, 'destination':destination}))
        return render(request, 'Error_page.html', {'message':form.errors['err']})
    
    
