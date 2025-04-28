import logging

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework . response import Response
from rest_framework import status


from .models import Navbar, Product, PaintBudgetCalculator, Category, CustomInfo
from .choices import OBJECT_TYPE_CHOICES
from .serializers import NavbarSerializer, PaintBudgetCalculatorSerializer, ProductSerializer, CategorySerializer, \
    CustomSerializer

logger = logging.getLogger(__name__)

class NavbarViewSet(viewsets.ModelViewSet):
    serializer_class = NavbarSerializer

    def get_queryset(self):
        """
        Return the base queryset (only filter, no HTTP Response here).
        """
        object_type = self.request.query_params.get('object_type', '').strip()
        if object_type:
            return Navbar.objects.filter(object_type=object_type)
        return Navbar.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Override list to add validation and custom error responses.
        """
        object_type = self.request.query_params.get('object_type', '').strip()

        if object_type and object_type not in dict(OBJECT_TYPE_CHOICES):
            return Response({'error': 'Invalid object_type provided.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({"error": "No galleries found for the provided object_type."}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PaintBudgetCalculatorViewSet(viewsets.ModelViewSet):
    queryset = PaintBudgetCalculator.objects.all()
    serializer_class = PaintBudgetCalculatorSerializer

    def validate_request_data(self, data):
        user_info_data = data.get("user_info")
        if not user_info_data:
            raise ValidationError("user_info is required.")

        if user_info_data.get("object_type") != "userinfo":
            raise ValidationError("Invalid object_type. Must be 'userinfo'.")

        metadata = user_info_data.get("metadata")
        if not isinstance(metadata, dict):
            raise ValidationError("metadata must be a valid JSON object.")

        required_fields = ["area_type", "surface_condition", "selected_product", "entered_area"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}.")

        return metadata

    def create(self, request, *args, **kwargs):
        """
        Creates a PaintBudgetCalculator entry along with related Gallery (user info) data.
        """
        try:
            metadata = self.validate_request_data(request.data)

            navbar = Navbar.objects.create(
                object_type="userinfo",
                metadata=metadata,
            )
            logger.debug(f"Navbar created with ID: {navbar.id}")

            paint_data = {
                "area_type": request.data["area_type"],
                "surface_condition": request.data["surface_condition"],
                "selected_product": request.data["selected_product"],
                "entered_area": request.data["entered_area"],
                "navbar": navbar.id,
            }

            serializer = self.get_serializer(data=paint_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "message": "Paint budget and user info saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unexpected error occurred during PaintBudgetCalculator creation.")
            return Response({
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category')
        subcategory_name = self.request.query_params.get('subcategory')

        if not category_name or not subcategory_name:
            raise ValidationError("Both 'category' and 'subcategory' are required.")

        queryset = Product.objects.filter(category__name=category_name, category__subcategory_name=subcategory_name)

        if not queryset.exists():
            raise NotFound(detail="No products found for the specified category and subcategory.")

        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer

    def get_queryset(self):
        try:
            return Category.objects.all().order_by('name')
        except Exception as e:

            raise Exception(f"An error occurred while fetching categories: {str(e)}")


class CustomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CustomSerializer

    def get_queryset(self):
        name_param = self.request.query_params.get('name')

        if name_param:
            queryset = CustomInfo.objects.filter(name=name_param).order_by('name')

            if not queryset.exists():
                raise NotFound("name not found ")
            return queryset

        raise ValidationError("The 'name' parameter is required.")
