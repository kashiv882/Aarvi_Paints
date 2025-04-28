from rest_framework import serializers
from . models import *

class NavbarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar
        fields = ['object_type', 'metadata', 'url']

class PaintBudgetCalculatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaintBudgetCalculator
        fields = ['area_type','surface_condition','selected_product','entered_area','navbar']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'subcategory_name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = [ 'title', 'keyfeature', 'description', 'category', 'url']

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomInfo
        fields = ["name" , "additional_info"]

