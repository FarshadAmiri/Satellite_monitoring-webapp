from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import pytz
from users.models import User
from fetch_data.utilities.tools import xyz2bbox_territory, bbox_geometry_calculator, coords_2_xyz_newton
import datetime

class PresetArea(models.Model):
    lon_min = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat_min = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon_max = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat_max = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    
    width =  models.IntegerField(null=True, blank=True,)
    height = models.IntegerField(null=True, blank=True,)
    area = models.BigIntegerField(null=True, blank=True,)

    x_min_z14 = models.IntegerField(null=True, blank=True,)
    x_max_z14 = models.IntegerField(null=True, blank=True,)
    y_min_z14 = models.IntegerField(null=True, blank=True,)
    y_max_z14 = models.IntegerField(null=True, blank=True,)

    tag = models.CharField(max_length=128, primary_key=True,)
    description = models.TextField(max_length=800, null=True, blank=True,)
    
    def save(self, *args, **kwargs):
        coords = (self.lon_min, self.lat_min, self.lon_max, self.lat_max)
        self.width, self.height, self.area = list(map(int, bbox_geometry_calculator(coords)))
        x_range_z14, y_range_z14, _ = coords_2_xyz_newton(coords, 14)
        (self.x_min_z14, self.x_max_z14), (self.y_min_z14, self.y_max_z14) = x_range_z14, y_range_z14
        super(PresetArea, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag
    
    def lonlat(self):
        return f"[{self.lon_min}, {self.lat_min}, {self.lon_max}, {self.lat_max}]"

    def x_range_z14(self):
        return (int(self.x_min_z14), int(self.x_max_z14))
    
    def y_range_z14(self):
        return (int(self.y_min_z14), int(self.y_max_z14))
    
    def wgs84_coords(self):
        try:
            return f"{self.lon_min:.6f}, {self.lat_min:.6f}, {self.lon_max:.6f}, {self.lat_max:.6f}"
        except:
            return "-"

class WaterCraft(models.Model):
    watercraft_type = models.CharField(max_length=64, default="Shipcraft")
    name = models.CharField(primary_key=True, max_length=64)
    length_min = models.FloatField(null=True)
    length_max = models.FloatField(null=True)
    color = models.CharField(null=True, max_length=16)

    def __str__(self):
        return f'{self.name}'


class SatteliteImage(models.Model):
    MOSAICKING_ORDER_TYPES = [('mostRecent', 'mostRecent'), ('leastCC', 'leastCC'), ('leastRecent', 'leastRecent')]
    DATA_SOURCES = [("SENTINEL2_L2A", "Sentinel2_L2A"), ("SENTINEL2_L1C", "Sentinel2_L1C")]
    
    image_path = models.URLField(primary_key=True, null=False, blank=False, default="Unknown")
    annotated_image_path = models.URLField(null=True, blank=True)

    bbox_lon1 = models.FloatField(null=True, blank=True)
    bbox_lat1 = models.FloatField(null=True, blank=True)
    bbox_lon2 = models.FloatField(null=True, blank=True)
    bbox_lat2 = models.FloatField(null=True, blank=True)

    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    zoom = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50)])

    area_tag = models.ForeignKey(PresetArea, related_name='area_tag', on_delete=models.SET_NULL, null=True, blank=True)
    
    time_from = models.DateField(null=True)
    time_to = models.DateField(null=True)
    # mosaicking_order = models.CharField(max_length=50, choices=MOSAICKING_ORDER_TYPES)
    # maxcc = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    data_source = models.CharField(max_length=50, choices=DATA_SOURCES)

    description = models.CharField(max_length=250)
    date_fetched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.image_path}'
    
    def original_image_size(self):
        return self.original_image.size
    
    def annotated_image_size(self):
        return self.annotated_image.size

    def wgs84_coords(self):
        return f"{self.bbox_lon1:.6f}, {self.bbox_lat1:.6f}, {self.bbox_lon2:.6f}, {self.bbox_lat2:.6f}"
    

class CoordsMap(models.Model):

    lon_min = models.FloatField()
    lon_max = models.FloatField()
    lat_min = models.FloatField()
    lat_max = models.FloatField()

    x = models.IntegerField()
    y = models.IntegerField()
    zoom = models.IntegerField()

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, zoom: {self.zoom}'


class QueuedTask(models.Model):
    TASK_TYPES = [('fetch', 'fetch'), ('infer', 'inference'), ('fetch_infer', 'fetch_and_inference')]
    TASK_STATUS = [('fetching', 'fetch_in_progress'), ('fetched', 'fetched'), ('inferencing', 'inference_in_progress'), ('inferenced', 'inferenced')]

    task_id = models.CharField(primary_key=True, max_length=255)
    is_parent = models.BooleanField(null=True)
    child_task = models.ManyToManyField("self", null=True, symmetrical=False, related_name='parent_task',)
    user_queued = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    task_type = models.CharField(max_length=128, choices=TASK_TYPES)
    task_status = models.CharField(max_length=128, choices=TASK_STATUS)
    fetch_progress = models.IntegerField(null=True, blank=True)

    area_tag = models.ManyToManyField(PresetArea)
    lon_min = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat_min = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon_max = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    lat_max = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])

    zoom = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50)])
    x_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    x_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    y_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    y_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    
    time_from = models.DateField()
    time_to = models.DateField()

    # time_queued = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(hours=3, minutes=30))
    # time_queued = models.DateTimeField(default=timezone.localtime(timezone.now()))
    time_queued = models.DateTimeField(auto_now_add=True)
    task_description = models.CharField(max_length=256)
    inference_result = models.JSONField(null=True, blank=True)


class DetectedObject(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    task = models.ManyToManyField(QueuedTask, null=True, related_name="detected_objects")
    image = models.ForeignKey(SatteliteImage, related_name='image_id', on_delete=models.CASCADE)
    
    lon = models.FloatField(null=True,)
    lat = models.FloatField(null=True,)

    time_from = models.DateField(null=True,)
    time_to = models.DateField(null=True,)
    object_type = models.ForeignKey(WaterCraft, null=True, related_name="detected_objects", on_delete=models.CASCADE)
    confidence = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    length = models.FloatField(null=True, blank=True)
    awake = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.id}'