import logging
import json
from django.views.decorators.csrf import csrf_exempt

from django.contrib.messages.storage import default_storage
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework . response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .choices import Home_Type_CHOICES



from .common import create_user_info, validate_request_data
from .forms import HomeInteriorForm
from .models import PaintBudgetCalculator, Category, ColourPalette, Parallax, Brochure, AdditionalInfo, \
    UserInfo, Product, Banner, Home, AdminContactDetails, WaterProofCalculator, AboutUs, \
    Setting  # CustomInfo ,Navbar,  AboutUs
from .choices import ADDITIONAL_INFO_TYPE_CHOICES, SOURCE_CHOICES, ALLOWED_SOURCES
from .serializers import PaintBudgetCalculatorSerializer, ProductSerializer, CategorySerializer, \
    ParallaxSerializer, BrochureSerializer,ColourPaletteSerializer,CustomTokenObtainPairSerializer, \
    AdditionalInfoSerializer, BannerSerializer, UserInfoSerializer, \
  AdminContactDetailsSerializer, \
    WaterProofCalculatorSerializer, AboutUsSerializer,HomeWaterProfSerializer,HomeExteriorSerializer,HomeInteriorSerializer,SettingSerializer \
 
     # CustomSerializer ,NavbarSerializer ,AboutUsSerializer


logger = logging.getLogger(__name__)
VALID_HOME_TYPES = [choice[0] for choice in Home_Type_CHOICES]

class PaintBudgetCalculatorViewSet(viewsets.ModelViewSet):
    queryset = PaintBudgetCalculator.objects.all()
    serializer_class = PaintBudgetCalculatorSerializer

    def create(self, request, *args, **kwargs):
        try:
            metadata = validate_request_data(
                request.data,
                ["area_type", "surface_condition", "selected_product", "entered_area"]
            )
            user_info = create_user_info(metadata, source="paint_budget")

            data = {
                "area_type": request.data["area_type"],
                "surface_condition": request.data["surface_condition"],
                "selected_product": request.data["selected_product"],
                "entered_area": request.data["entered_area"],
                "userinfo": user_info.id,
            }

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": "Paint budget and user info saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error occurred.")
            return Response({"message": "An unexpected error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Product.objects.all()

        # Get filters from request query parameters
        category_name = self.request.query_params.get('category__name')
        subcategory = self.request.query_params.get('subcategory')

        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)

        if subcategory:
            queryset = queryset.filter(subcategory__icontains=subcategory)

        if not queryset.exists():
            raise NotFound({"error": "No products found."})

        return queryset

class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all().order_by('name')
        if not queryset.exists():
            raise NotFound({"error": "No categories found."})
        return queryset

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        queryset = Setting.objects.all().order_by('name')
        if not queryset.exists():
            raise NotFound({"error": "No categories found."})
        return queryset


class AdminContactViewSet(viewsets.ModelViewSet):

    queryset = AdminContactDetails.objects.all()
    serializer_class = AdminContactDetailsSerializer


    def get_queryset(self):
        queryset = AdminContactDetails.objects.all()
        if not queryset.exists():
            raise NotFound({"error": "No admin contact details found."})
        return queryset


class BannerViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        banner_type = self.request.query_params.get('type', '').strip()
        banners = Banner.objects.filter(type=banner_type)

        if banner_type:
            if not banners.exists():
                raise ValidationError({"error": "No banners found for the provided type."})
            return banners

        return Banner.objects.all()


class ColourPaletteViewSet(viewsets.ModelViewSet):
    queryset = ColourPalette.objects.all()
    serializer_class = ColourPaletteSerializer

    def get_queryset(self):
        queryset = ColourPalette.objects.all()
        type_param = self.request.query_params.get('type')
        if type_param:
            queryset = queryset.filter(type=type_param)
        return queryset
        

        # queryset = ColourPalette.objects.all()
        # if not queryset.exists():
        #     raise NotFound({"error": "No parallax objects found."})
        # return queryset

        
    



class ParallaxViewSet(viewsets.ModelViewSet):
    serializer_class = ParallaxSerializer
    queryset = Parallax.objects.all()

    def get_queryset(self):
        queryset = Parallax.objects.all()
        if not queryset.exists():
            raise NotFound({"error": "No parallax objects found."})
        return queryset


class BrochureViewSet(viewsets.ModelViewSet):
    serializer_class = BrochureSerializer
    queryset = Brochure.objects.all()

    def get_queryset(self):
        queryset = Brochure.objects.all()
        if not queryset.exists():
            raise NotFound({"error": "No brochures found."})
        return queryset



class AdditionalInfoViewSet(viewsets.ModelViewSet):
    serializer_class = AdditionalInfoSerializer
    def get_queryset(self):
        type_param = self.request.query_params.get('type', None)
        print(type_param)

        if type_param:

            valid_types = dict(ADDITIONAL_INFO_TYPE_CHOICES).keys()
            if type_param not in valid_types:
                raise ValidationError({"error": "Type not found. Valid types are: Inspiration, TESTIMONIAL,Calculator,WATER_CALCULATOR."})


            queryset = AdditionalInfo.objects.filter(type=type_param)
            print("QUERYSET COUNT:", queryset.count())

            if not queryset.exists():
                raise NotFound({"error": f"No additional info found for type {type_param}."})

            return queryset

        return AdditionalInfo.objects.all()




class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    print("the queryset is ",queryset)
    serializer_class = UserInfoSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            print("the data",data)
            source = data.get("source")

            if source not in dict(SOURCE_CHOICES):
                raise ValidationError(f"Invalid source. Must be one of: {', '.join(dict(SOURCE_CHOICES).keys())}.")

            if source not in ALLOWED_SOURCES:
                raise ValidationError(f"Creation is only allowed for source: 'quote' or 'BookAppointment'.")

            serializer = self.get_serializer(data=data)
            print("serializers",serializer)
            serializer.is_valid(raise_exception=True)


            self.perform_create(serializer)

            return Response({
                "message": f"User info from {source} saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error occurred during user info creation.")
            return Response({
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class HomeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

    def get_queryset(self):
        home_type = self.request.query_params.get('type', '').strip()

        if home_type and home_type not in VALID_HOME_TYPES:
            raise ValidationError({"error": "Invalid type provided."})

        queryset = Home.objects.filter(type=home_type) if home_type else Home.objects.all()

        if not queryset.exists():
            raise NotFound({"error": "No homes found for the provided type."})

        return queryset

    def get_serializer_class(self):
        home_type = self.request.query_params.get('type', '').strip()

        if home_type == 'WaterProf':
            return HomeWaterProfSerializer
        elif home_type == 'Exterior':
            return HomeExteriorSerializer
        elif home_type == 'Interior':
            return HomeInteriorSerializer
        elif home_type == '':

            raise ValidationError({"error": "Query parameter 'type' is required."})
        else:
            raise ValidationError({"error": "Invalid type provided."})
        

class WaterProofCalculatorViewSet(viewsets.ModelViewSet):
    queryset = WaterProofCalculator.objects.all()
    serializer_class = WaterProofCalculatorSerializer

    def create(self, request, *args, **kwargs):
        try:
            metadata = validate_request_data(request.data, ["description", "surface_condition", "selected_product", "entered_area"])
            user_info = create_user_info(metadata, source="WaterProof")

            data = {
                "description": request.data["description"],
                "surface_condition": request.data["surface_condition"],
                "selected_product": request.data["selected_product"],
                "entered_area": request.data["entered_area"],
                "userinfo": user_info.id,
            }

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": "Waterproof data and user info saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error occurred.")
            return Response({"message": "An unexpected error occurred.", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class CustomViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = CustomSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['name']
#
#     def get_queryset(self):
#         queryset = CustomInfo.objects.all()
#
#         return queryset

class AboutUsViewSet(viewsets.ModelViewSet):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.all()

    def get_queryset(self):
        return AboutUs.objects.all()


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            subcategories = category.subcategory_names or []
        except Category.DoesNotExist:
            subcategories = []
    else:
        subcategories = []

    return JsonResponse({'subcategories': subcategories})

# class NavbarViewSet(viewsets.ModelViewSet):
#     serializer_class = NavbarSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['object_type']
#
#     def list(self, request, *args, **kwargs):
#         object_type = self.request.query_params.get('object_type', '').strip()
#
#         if object_type and object_type not in dict(OBJECT_TYPE_CHOICES):
#             return Response({'error': 'Invalid object_type provided.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         queryset = self.filter_queryset(self.get_queryset())
#
#         if not queryset.exists():
#             return Response({"error": "No galleries found for the provided object_type."}, status=status.HTTP_404_NOT_FOUND)
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

def create_home_interior(request):
    if request.method == 'POST':
        form = HomeInteriorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the HomeInterior instance with image URLs and other fields
            return redirect('home_interior_success')  # Redirect to success page (or wherever)
    else:
        form = HomeInteriorForm()  # Initialize an empty form

    return render(request, 'home_interior_form.html', {'form': form})


def upload_image_url(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        path = default_storage.save(f'uploads/{file.name}', file)
        url = default_storage.url(path)
        return JsonResponse({'url': url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print("Raw body:", request.body)
        print("Parsed data:", request.data)
        return super().post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    pass


# @csrf_exempt  # Disable CSRF for this specific view
# @api_view(['POST'])
# def token_obtain_pair_no_csrf(request):
#     print("Reached token_obtain_pair_no_csrf view")
#     serializer = TokenObtainPairSerializer(data=request.data)
#     breakpoint()
#     if serializer.is_valid():
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @csrf_exempt
# @api_view(['POST'])
# def generate_jwt_token(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password)
#     if user is not None:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def print_product_schema_view(request):
    schema = {
        field.name: field.get_internal_type()
        for field in Product._meta.fields
    }
    return JsonResponse(schema)