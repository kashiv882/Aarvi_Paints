from rest_framework import serializers
from . models import *

class Galleryserializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class PaintBudgetCalculatorSerializer(serializers.ModelSerializer):
    class Meta:
        model =  PaintBudgetCalculator
        fields = ['id', 'area_type', 'surface_condition', 'selected_product', 'entered_area','gallery']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

