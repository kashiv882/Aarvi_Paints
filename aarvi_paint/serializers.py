from rest_framework import serializers
from .models import *

# class NavbarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Navbar
#         fields = ['object_type', 'details', 'url']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['name', 'phone_number', 'email', 'pincode', 'type', 'description','source']


class PaintBudgetCalculatorSerializer(serializers.ModelSerializer):
    """"These oth banners and banners variable will be removed once the admin panel will be fully functional """
    userinfo = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), write_only=True)
    userinfo_detail = UserInfoSerializer(source='userinfo', read_only=True)

    class Meta:
        model = PaintBudgetCalculator
        fields = ['id', 'area_type', 'surface_condition', 'selected_product', 'entered_area', 'userinfo', 'userinfo_detail']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'subcategory_names']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['title', 'keyfeature', 'description', 'category', 'url']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'type', 'placement_location', 'short_description', 'url']

class ColourPaletteFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColourPalette
        fields = ['title', 'description', 'url']

class ColourPaletteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColourPalette
        fields = ['colour_code', 'colour_code_category']

class ParallaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parallax
        fields = ['title', 'sub_title', 'description', 'url', 'priority']

class BrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brochure
        fields = ['url', 'uploaded_pdf']

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['title','sub_title', 'description', 'url', 'details']

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['type', 'title', 'description', 'url','details']

class AdminContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactDetails
        fields = ['location', 'phone_number', 'email', 'google_link', 'social_media_links']


class HomeSerializer(serializers.ModelSerializer):
     banners = BannerSerializer()

     class Meta:
        model = Home
        fields = [ 'type', 'banners', 'category_name', 'subcategory_name'
                 ,'category_images', 'type_images', 'type_description', 'title_type']



class WaterProofCalculatorSerializer(serializers.ModelSerializer):
    """"These oth banners and banners variable will be removed once the admin panel will be fully functional """
    userinfo = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), write_only=True)
    userinfo_detail = UserInfoSerializer(source='userinfo', read_only=True)

    class Meta:
        model = WaterProofCalculator
        fields = [ 'id',
            'surface_condition','selected_product','entered_area','description','userinfo','userinfo_detail',]
