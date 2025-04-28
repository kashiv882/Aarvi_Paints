import uuid
from django.db import models
from .choices import *


class Navbar(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_type = models.CharField(max_length=200 , choices= OBJECT_TYPE_CHOICES )
    metadata = models.JSONField()
    url =  models.JSONField(null=True)


class PaintBudgetCalculator(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    navbar = models.ForeignKey('Navbar', on_delete=models.CASCADE, related_name='paint_budgets')


class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100)


class Product(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    keyfeature = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='category')
    url = models.JSONField()


class CustomInfo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    additional_info = models.JSONField(blank=True, null=True)








