from django import forms
from django.forms import ModelForm
from .models import *

class SentinelFetchForm(forms.Form):
    # CITIES = City.objects.only('name')
    # origin = forms.ModelChoiceField(queryset=CITIES)
    # destination = forms.ModelChoiceField(queryset=CITIES)
    
    def clean_destination(self):
        destination = self.cleaned_data['destination']
        origin = self.cleaned_data['origin']
        if (destination != origin):
            return destination
        else:
            message = 'Origin and Destination cannot be the same'
            self.errors['err'] = message