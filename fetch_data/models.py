from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from fetch_data.utilities.tools import xyz2bbox, xyz2bbox_territory

class PresetArea(models.Model):
    bbox_lon1 = models.FloatField(null=True, blank=True)
    bbox_lat1 = models.FloatField(null=True, blank=True)
    bbox_lon2 = models.FloatField(null=True, blank=True)
    bbox_lat2 = models.FloatField(null=True, blank=True)

    zoom = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(50)])
    x_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    x_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    y_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])
    y_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(500000)])

    tag = models.CharField(max_length=128, primary_key=True,)
    description = models.TextField(max_length=800, null=True, blank=True,)

    # def __str__(self):
    #     return f'{self.tag}'
    
    # def validate_x_max(self, value):
    #     pass

    # def validate_y_max(self, value):
    #     pass

    def save(self, *args, **kwargs):
        self.bbox_lon1, self.bbox_lat1, self.bbox_lon2, self.bbox_lat2 = xyz2bbox_territory((self.x_min, self.x_max), (self.y_min, self.y_max), self.zoom)
        super(PresetArea, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag

    def x_range(self):
        return f"{self.x_min:.0f} : {self.x_max:.0f}"
    
    def y_range(self):
        return f"{self.y_min:.0f} : {self.y_max:.0f}"
    
    def wgs84_coords(self):
        try:
            return f"{self.bbox_lon1:.6f}, {self.bbox_lat1:.6f}, {self.bbox_lon2:.6f}, {self.bbox_lat2:.6f}"
        except:
            return "-"

class WaterCraft(models.Model):
    watercraft_type = models.CharField(max_length=64)
    name = models.CharField(primary_key=True, max_length=64)
    length_min = models.FloatField()
    length_max = models.FloatField()
    color = models.CharField(max_length=16)

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
    zoom = models.FloatField(null=True, blank=True)

    Area_tag = models.ForeignKey(PresetArea, related_name='area_tag', on_delete=models.SET_NULL, null=True, blank=True)
    
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


class DetectedObject(models.Model):
    pk = models.CharField(primary_key=True, max_length=128)
    image = models.ForeignKey(SatteliteImage, related_name='image_id', on_delete=models.CASCADE)
    
    lon = models.FloatField()
    lat = models.FloatField()
    x = models.IntegerField()
    y = models.IntegerField()
    zoom = models.IntegerField()

    time_from = models.DateField()
    time_to = models.DateField()
    object_type = models.ForeignKey(WaterCraft, null=True, related_name="detected_objects", on_delete=models.CASCADE)
    confidence = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    length = models.FloatField(null=True, blank=True)
    awake = models.BooleanField(null=True)
    # ships_coords =  models.CharField(validators=)
    # ships_lengths = models.CharField(validators=)
    # ships_scores = models.CharField(validators=)
    # ships_bbox_h = models.FloatField()
    # ships_bbox_w = models.FloatField()

    # object_id = models.PositiveIntegerField()
    # object_type = models.CharField(max_length=20)
    # object_score = models.FloatField()
    # object_length = models.FloatField()
    # object_bbox_h = models.FloatField()
    # object_bbox_w = models.FloatField()
    # object_bbox_x = models.FloatField()
    # object_bbox_y = models.FloatField()

    def __str__(self):
        return f'{self.id}'
    

