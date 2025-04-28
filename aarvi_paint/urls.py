from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NavbarViewSet, ProductViewSet, PaintBudgetCalculatorViewSet, CategoryViewSet, CustomViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'paint-budget-calculator', PaintBudgetCalculatorViewSet,basename='paint-budget-calculator')
router.register(r'navbar', NavbarViewSet, basename='navbar')
router.register(r'custom' , CustomViewSet , basename='custom')


urlpatterns = [
    path('', include(router.urls)),
]
