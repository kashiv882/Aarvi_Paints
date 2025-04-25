import uuid
from django.db import models
from .choices import *
class Gallery(models.Model):
    # OBJECT_TYPE_CHOICES = [
    #     ('banners', 'Banners'),
    #     ('userinfo', 'User Info'),
    #     ('colourpalate', 'Color Palate'),
    #     ('parallax', 'Parallax'),
    #     ('brochure', 'Brochure'),
    # ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_type = models.CharField(max_length=200 , choices= OBJECT_TYPE_CHOICES )
    metadata = models.JSONField()
    url = models.CharField(max_length=200)

class PaintBudgetCalculator(models.Model):
    # AREA_TYPE_CHOICES = [
    #     ('interior', 'Interior'),
    #     ('exterior', 'Exterior'),
    # ]
    #
    # SURFACE_CONDITION_CHOICES = [
    #     ('new', 'New'),
    #     ('repaint', 'Repaint'),
    # ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE, related_name='paint_budgets')



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    keyfeature = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='inits')
    url = models.CharField(max_length=200)





