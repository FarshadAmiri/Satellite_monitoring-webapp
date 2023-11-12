from django.contrib import admin
from .models import *
from django.contrib import admin, messages
import datetime as dt

# admin.site.register(City)
# admin.site.register(SatteliteImage)
# admin.site.register(SatteliteImageObject)


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


@admin.register(PresetArea)
class PresetAreasAdmin(admin.ModelAdmin):
    list_display = ('tag', "x_range", "y_range", "zoom", "bbox_lon1", "bbox_lat1", "bbox_lon2", "bbox_lat2")
    list_display_links = ['tag']
    ordering = ['tag']
    list_filter = [('zoom', custom_titled_filter('zoom')),]
    search_fields = ["tag", "x_min", "x_max", "y_min", "y_max", "bbox_lon1", "bbox_lat1", "bbox_lon2", "bbox_lat2",]
    # list_editable = ['tag',]
    readonly_fields = ["bbox_lon1", "bbox_lat1", "bbox_lon2", "bbox_lat2", "wgs84_coords"]
    # date_hierarchy = 'datetime'

    fieldsets = (
        ("Area specifications", {
            "fields": ("tag", "zoom", ("x_min", "x_max"), ("y_min", "y_max"),)
        }),
        ("Coordinations & info", {
            'fields':('bbox_lon1', 'bbox_lat1', "bbox_lon2", "bbox_lat2",("wgs84_coords"))
        }),
        # ('More info' , {
        #     'classes':('collapse',), 'fields':('description')
        # }),
    )

    # def shift_by_2hours(self, request, queryset):
    #     for f in queryset:
    #         f.datetime = f.datetime + dt.timedelta(hours=2)
    #         f.save()
    #     self.message_user(
    #         request, f"{queryset.count()} flights shifted by 2 hours", messages.SUCCESS
    #     )

    # actions = ['shift_by_2hours']
    # shift_by_2hours.short_description = 'Postpone flight(s) for 2 hours'


@admin.register(SatteliteImage)
class SatteliteImageAdmin(admin.ModelAdmin):
    list_display = ["time_from","time_to", 'x','y','zoom', "Area_tag", "image_path", "date_fetched"]
    list_display_links = ['image_path',]
    ordering = ['date_fetched']
    list_filter = [('zoom', custom_titled_filter('zoom')), ('date_fetched', custom_titled_filter('date_fetched')),
                   ('time_from', custom_titled_filter('time_from')), ('time_to', custom_titled_filter('time_to'))]
    search_fields = ["x", "y", "zoom", "time_from", "time_to", "bbox_lon1", "bbox_lat1", "bbox_lon2", "bbox_lat2", "Area_tag"]
    # list_editable = ['tag',]
    readonly_fields = ["bbox_lon1", "bbox_lat1", "bbox_lon2", "bbox_lat2", "wgs84_coords"]
    # date_hierarchy = 'datetime'

    fieldsets = (
        ("Area specifications", {
            "fields": (("Area_tag", "zoom"), ("x", "y"))
        }),
        ("Time specifications", {
            "fields": ("time_from", "time_to")
        }),
        ("Coordinations & info", {
            'fields':('bbox_lon1', 'bbox_lat1', "bbox_lon2", "bbox_lat2", ("wgs84_coords"))
        }),
    )

# @admin.register(DetectedObject)
# # class SatteliteImageObjectAdmin(admin.ModelAdmin):
# #     # list_display = ('image', 'annotated_image', 'n_total_ships', 'n_navy', 'n_oil_tanker', 'n_cargo')
# #     # ordering = ['pk']