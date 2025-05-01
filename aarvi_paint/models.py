import uuid
from django.db import models
from .choices import *


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class PaintBudgetCalculator(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES_PAINT_BUDGET)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    userinfo= models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='paint_budgets')


class Category(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100)


class Product(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    keyfeature = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field='id', related_name='category')
    url = models.JSONField()


class Banner(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    placement_location = models.CharField(max_length=200)
    short_description = models.TextField()
    url = models.JSONField(default=dict, blank=True)


class UserInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    pincode = models.CharField(max_length=100)
    type = models.CharField(max_length=200,null = True)
    description = models.TextField()
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)


class ColourPalette(TimeStampedModel):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    colour_code = models.IntegerField()
    colour_code_category = models.CharField(max_length=200)
    url = models.JSONField(default=dict, blank=True)


class Parallax(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.JSONField(default=dict, blank=True)
    priority = models.IntegerField()


class Brochure(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.JSONField(default=dict, blank=True)
    uploaded_pdf = models.CharField(max_length=200)


class AdditionalInfo(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=200 , choices=ADDITIONAL_INFO_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.JSONField(default=dict, blank=True)
    details = models.JSONField(default=dict, blank=True)


class Home(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=200 , choices=Home_Type_CHOICES)
    banners = models.ForeignKey(Banner,on_delete=models.CASCADE,related_name="homes")
    category_name = models.CharField(max_length=100)
    subcategory_name = models.CharField(max_length=100)
    category_images = models.JSONField(default=dict, blank=True)
    type_images = models.JSONField(default=dict, blank=True)
    type_description = models.TextField()
    title_type = models.CharField(max_length=200)


class AdminContactDetails(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    google_link = models.URLField()
    social_media_links = models.JSONField(default=list, blank=True)


class WaterProofCalculator(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surface_condition = models.CharField(max_length=50, choices=SURFACE_CONDITION_CHOICES_WATERPROOF)
    selected_product = models.CharField(max_length=100)
    entered_area = models.FloatField(help_text="Enter area in square meters")
    userinfo = models.ForeignKey('UserInfo', on_delete=models.CASCADE, related_name='waterproof_calculations')
    description = models.TextField()




# class CustomInfo(models.Model):
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     additional_info = models.JSONField(blank=True, null=True)
#
#
# class ObjectType(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     variable_name = models.CharField(max_length=100, unique=True)
#     fields = models.JSONField(default=dict)

# class AboutUs(TimeStampedModel):
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=200)
#     sub_title = models.CharField(max_length=200)
#     description = models.TextField()
#     url = models.JSONField(default=dict, blank=True)
#     details = models.JSONField(default=dict, blank=True)


# class Navbar(TimeStampedModel):
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     object_type = models.CharField(max_length=200 , choices= OBJECT_TYPE_CHOICES )
#     details= models.JSONField()
#     url =  models.JSONField(null=True)





