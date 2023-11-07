from django import forms
from django.forms import ModelForm
from .models import *
import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput


class SentinelFetchForm(forms.Form):
    class Meta:
        # model = SatteliteImage
        # fields = "__all__"
        widgets = {
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput(range_from="start_date"),
            'base_date': DatePickerInput()
        }
    # CITIES = City.objects.only('name')
    # origin = forms.ModelChoiceField(queryset=CITIES)
    # destination = forms.ModelChoiceField(queryset=CITIES)
    x_min = forms.IntegerField(min_value=0, max_value=500000,)
    x_max = forms.IntegerField(min_value=0, max_value=500000)
    y_min = forms.IntegerField(min_value=0, max_value=500000)
    y_max = forms.IntegerField(min_value=0, max_value=500000)
    zoom = forms.IntegerField(min_value=0, max_value=50)
    start_date = forms.DateField(widget=DatePickerInput(), required=False)
    end_date = forms.DateField(widget=DatePickerInput(),  required=False)
    base_date = forms.DateField(widget=DatePickerInput(), required=False)
    n_days_before_base_date = forms.IntegerField(min_value=0, max_value=365,  required=False)
    overwrite_repetitious = forms.BooleanField(required=False)
    image_store_path = forms.CharField( required=False)

    def clean_x_min(self):
        x_min = self.cleaned_data['x_min']
        if x_min < 0 or x_min > 500000:
            raise forms.ValidationError('Invalid x_min value')
        return x_min

    def clean_x_max(self):
        x_max = self.cleaned_data['x_max']
        if x_max < 0 or x_max > 500000:
            raise forms.ValidationError('Invalid x_max value')
        return x_max

    def clean_y_min(self):
        y_min = self.cleaned_data['y_min']
        if y_min < 0 or y_min > 500000:
            raise forms.ValidationError('Invalid y_min value')
        return y_min

    def clean_y_max(self):
        y_max = self.cleaned_data['y_max']
        if y_max < 0 or y_max > 500000:
            raise forms.ValidationError('Invalid y_max value')
        return y_max

    def clean_zoom(self):
        zoom = self.cleaned_data['zoom']
        if zoom < 0 or zoom > 50:
            raise forms.ValidationError('Invalid zoom value')
        return zoom

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date is not None:
            if start_date > datetime.datetime.now().date():
                raise forms.ValidationError('Start date cannot be a date in future!')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if (start_date != None) and (end_date != None):
            if end_date > datetime.datetime.now().date():
                raise forms.ValidationError('End date cannot be a date in future!')
            if end_date < start_date:
                raise forms.ValidationError('End date cannot be greater than Start date!')
        return end_date

    def clean_n_days_before_base_date(self):
        n_days_before_base_date = self.cleaned_data['n_days_before_base_date']
        if n_days_before_base_date != None:
            if n_days_before_base_date < 0 or n_days_before_base_date > 365:
                raise forms.ValidationError('Invalid n_days_before_base_date value')
        return n_days_before_base_date

    # def clean_base_date(self):
    #     base_date = self.cleaned_data['base_date']
    #     if base_date < datetime.datetime.now():
    #         raise forms.ValidationError('Base date cannot be in the past')
    #     return base_date

    # def clean_overwrite_repetitious(self):
    #     overwrite_repetitious = self.cleaned_data['overwrite_repetitious']
    #     if overwrite_repetitious not in ['true', 'false']:
    #         raise forms.ValidationError('Invalid overwrite_repetitious')