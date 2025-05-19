import re
from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed

# class NavbarSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Navbar
#         fields = ['object_type', 'details', 'url']


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['name', 'phone_number', 'email', 'pincode', 'type', 'description','source']

    def validate_phone_number(self, value):
        
        value=value.strip()
        print("value we have ",value)
        if not re.match(r'^[6-9]\d{9}$', value):
            raise serializers.ValidationError("Mobile number must be 10 digits and start with 6, 7, 8, or 9.")
        return value
    
    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Email must start with a letter and be a valid email address.")
        return value
            
    def validate_pincode(self, value):
        if not (value.isdigit() and len(value) == 6):
            raise serializers.ValidationError("The pin code should be exactly 6 digits.")
        return value



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
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = [
            'title',
            'subtitle',
            'short_description',
            'long_description',
            'keyfeature',
            'category',            
            'subcategory',
            'url',
            'colour_palate1',
            'colour_palate2'
        ]

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['title', 'type', 'placement_location', 'short_description', 'url']

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ['name','copyright','url','app_download_links','hide']
 
class ColourPaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColourPalette
        fields = ['title', 'description', 'url', 'side_Title', 'side_description', 'details','type']



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
        fields = ['title', 'description', 'details']

class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = ['type', 'title', 'description', 'url','details']

class AdminContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactDetails
        fields = ['location', 'phone_number', 'email', 'google_link', 'social_media_links']

class HomeWaterProfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['title', 'description', 'category_name', 'side_images']

class HomeExteriorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Home
            fields = ['title', 'description', 'category_name','category_images','type']

class HomeInteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['title', 'description', 'category_name', 'subcategory_name','category_images', 'type','type_images','type_description','title_type']


class WaterProofCalculatorSerializer(serializers.ModelSerializer):
    """"These oth banners and banners variable will be removed once the admin panel will be fully functional """
    userinfo = serializers.PrimaryKeyRelatedField(queryset=UserInfo.objects.all(), write_only=True)
    userinfo_detail = UserInfoSerializer(source='userinfo', read_only=True)

    class Meta:
        model = WaterProofCalculator
        fields = [ 'id',
            'surface_condition','selected_product','entered_area','description','userinfo','userinfo_detail',]


User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()
        if not user:
            raise AuthenticationFailed("User does not exist")

        if not user.check_password(password):
            raise AuthenticationFailed("Password is wrong")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled")

        data = super().validate(attrs)
        return data