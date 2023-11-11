from rest_framework import serializers
from .models import PresetArea

class TerritorySerializer(serializers.Serializer):
    preset_area = serializers.CharField(required=False)
    x_min = serializers.IntegerField(min_value=0, max_value=500000, required=False)
    x_max = serializers.IntegerField(min_value=0, max_value=500000, required=False)
    y_min = serializers.IntegerField(min_value=0, max_value=500000, required=False)
    y_max = serializers.IntegerField(min_value=0, max_value=500000, required=False)
    zoom = serializers.IntegerField(min_value=0, max_value=50, required=False)
    start_date = serializers.CharField(required=False)
    end_date = serializers.CharField(required=False)
    base_date = serializers.CharField(required=False)
    n_days_before_base_date = serializers.IntegerField(min_value=0, max_value=365,  required=False)
    overwrite_repetitious = serializers.CharField(required=False)
    # overwrite_repetitious = serializers.BooleanField(required=False)


    # def validate(self, data):
    #     if data.get('x_min', 0) > data.get('x_max', 0):
    #         raise serializers.ValidationError('x_max should be greater than x_min')
        
    #     if data.get('y_min', 0) > data.get('y_max', 0):
    #         raise serializers.ValidationError('y_max should be greater than y_min')
        
    #     if data.get('start_date', None) > data.get('end_date', None):
    #         raise serializers.ValidationError('start_date should be earlier than end_date')
        
    #     if (None in [data.get('x_min', None), data.get('x_max', None), data.get('y_min', None), data.get('y_max', None), data.get('zoom', None)]) and data.get('preset_area', False):
    #         raise serializers.ValidationError('Request should either contains a bundle of "x_min, x_max, y_min, y_max, zoom" or a preset_area name')
        
    #     if (None not in [data.get('x_min', None), data.get('x_max', None), data.get('y_min', None), data.get('y_max', None), data.get('zoom', None)]) and data.get('preset_area', False) != False:
    #         raise serializers.ValidationError('Request should either contains a bundle of "x_min, x_max, y_min, y_max, zoom" or a preset_area name - not both of them')
        
    #     if (None not in [data.get('start_date', None), data.get('end_date', None), data.get('base_date', None), data.get('n_days_before_base_date', None),]):
    #         raise serializers.ValidationError('Request should either contains of pair of "start_date, end_date" or "base_date, n_days_before_base_date"')
    #     return data

    # def validate_preset_area(self ,value):
    #     try:
    #         preset_area_instance = PresetArea.objects.get(tag=value)
    #     except PresetArea.DoesNotExist:
    #         raise serializers.ValidationError('Preset area "%s" does not exist' % value)
        
    #     return value

    # def validate_overwrite_repetitious(self, value):
    #     if value == "True":
    #         return True
    #     elif value in ["False" or None]:
    #         return False
    #     else:
    #         raise serializers.ValidationError('overwrite_repetitious should be either True or False')