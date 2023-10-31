from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class PresetArea(models.Model):
    tag = models.CharField(max_length=250)
    description = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.name}'


class SatteliteImage(models.model):
    MOSAICKING_ORDER_TYPES = [('mostRecent'), ('leastCC'), ('leastRecent')]
    DATA_COLLECTION = [("SENTINEL2_L2A"), ("SENTINEL2_L1C")]
    
    bbox_lon1 = models.FloatField(null=True, blank=True)
    bbox_lat1 = models.FloatField(null=True, blank=True)
    bbox_lon2 = models.FloatField(null=True, blank=True)
    bbox_lat2 = models.FloatField(null=True, blank=True)
    Area_tag = models.ForeignKey(PresetArea, related_name='area_tag', on_delete=models.SET_NULL, null=True, blank=True)
    
    time_start = models.DateField(null=True, blank=True)
    time_end = models.DateField()
    mosaicking_order = models.CharField(max_length=1, choices=MOSAICKING_ORDER_TYPES)
    maxcc = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    data_collection = models.CharField(max_length=1, choices=DATA_COLLECTION)
    
    original_image = models.ImageField(upload_to='images/', )
    annotated_image = models.ImageField(upload_to='images/', )
    
    ships_attr = models.JSONField()   #coords, score, bbox_dimensions, length
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
    
    description = models.CharField(max_length=250)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
    def original_image_size(self):
        return self.original_image.size
    
    def annotated_image_size(self):
        return self.annotated_image.size
