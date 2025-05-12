from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.views.decorators.csrf import csrf_exempt


from . import views
from .models import AdminContactDetails
from .views import ProductViewSet, PaintBudgetCalculatorViewSet, CategoryViewSet, BannerViewSet, ColourPaletteViewSet, \
    ParallaxViewSet, BrochureViewSet, AdditionalInfoViewSet, \
    UserInfoViewSet, HomeViewSet, AdminContactViewSet, \
    WaterProofCalculatorViewSet, AboutUsViewSet, SettingViewSet, \
    create_home_interior  # CustomViewSet NavbarViewSet,, AboutUsViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'paint-budget-calculator', PaintBudgetCalculatorViewSet,basename='paint-budget-calculator')
# router.register(r'navbar', NavbarViewSet, basename='navbar')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'colourpalettes', ColourPaletteViewSet, basename='colourpalette')
router.register(r'parallax', ParallaxViewSet, basename='parallax')
router.register(r'brochures', BrochureViewSet, basename='brochure')
router.register(r'aboutus', AboutUsViewSet, basename='aboutus')
router.register(r'additionalinfo', AdditionalInfoViewSet, basename='additionalinfo')
router.register(r'userinfo', UserInfoViewSet, basename='userinfo'),
router.register(r'home', HomeViewSet, basename='home'),
router.register(r'admincontectinfo', AdminContactViewSet, basename='admincontectinfo'),
router.register(r'waterproof',WaterProofCalculatorViewSet, basename='waterproof')
router.register(r'setting',SettingViewSet, basename='setting')



# router.register(r'custom' , CustomViewSet , basename='custom')


urlpatterns = [
    path('', include(router.urls)),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('home-interior/', create_home_interior, name='create_home_interior'),
    path('upload-image-url/', views.upload_image_url, name='upload_image_url'),
    
    path('api/token/', csrf_exempt(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', csrf_exempt(TokenRefreshView.as_view()), name='token_refresh'),
    
]
