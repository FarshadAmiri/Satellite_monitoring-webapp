from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PresetAreas(models.Model):
    bbox_lon1 = models.FloatField(null=True, blank=True)
    bbox_lat1 = models.FloatField(null=True, blank=True)
    bbox_lon2 = models.FloatField(null=True, blank=True)
    bbox_lat2 = models.FloatField(null=True, blank=True)

    tag = models.CharField(max_length=128, primary_key=True)
    description = models.TextField(max_length=800)

    def __str__(self):
        return f'{self.tag}'


class SatteliteImages(models.Model):
    MOSAICKING_ORDER_TYPES = [('mostRecent', 'mostRecent'), ('leastCC', 'leastCC'), ('leastRecent', 'leastRecent')]
    DATA_SOURCES = [("SENTINEL2_L2A", "Sentinel2_L2A"), ("SENTINEL2_L1C", "Sentinel2_L1C")]
    
    bbox_lon1 = models.FloatField(null=True, blank=True)
    bbox_lat1 = models.FloatField(null=True, blank=True)
    bbox_lon2 = models.FloatField(null=True, blank=True)
    bbox_lat2 = models.FloatField(null=True, blank=True)

    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)
    zoom = models.FloatField(null=True, blank=True)

    Area_tag = models.ForeignKey(PresetAreas, related_name='area_tag', on_delete=models.SET_NULL, null=True, blank=True)
    
    time_start = models.DateField(null=True, blank=True)
    time_end = models.DateField()
    # mosaicking_order = models.CharField(max_length=50, choices=MOSAICKING_ORDER_TYPES)
    # maxcc = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    data_source = models.CharField(max_length=50, choices=DATA_SOURCES)
    
    image_path = models.URLField(primary_key=True, null=False, blank=False, default="Unknown")
    description = models.CharField(max_length=250)
    date_fetched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
    
    def original_image_size(self):
        return self.original_image.size
    
    def annotated_image_size(self):
        return self.annotated_image.size
    

class SatteliteImageObjects(models.Model):
    image = models.ForeignKey(SatteliteImages, related_name='image_id', on_delete=models.CASCADE)
    annotated_image = models.ImageField(upload_to='images/', )
    
    ships_data = models.JSONField()   #coords, score, bbox_dimensions, length
    # ships_coords =  models.CharField(validators=)
    # ships_lengths = models.CharField(validators=)
    # ships_scores = models.CharField(validators=)
    # ships_bbox_h = models.FloatField()
    # ships_bbox_w = models.FloatField()

    n_total_ships = models.PositiveIntegerField()
    n_navy = models.PositiveIntegerField()
    n_oil_tanker = models.PositiveIntegerField()
    n_cargo = models.PositiveIntegerField()
    n_fishing = models.PositiveIntegerField()
    n_boat = models.PositiveIntegerField()

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