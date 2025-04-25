
from django.urls import path
from .views import GalleryView, PaintBudgetCalculatorView

urlpatterns = [
    path('gallery/', GalleryView.as_view(), name='gallery-by-object-type'),
    path('paint-budget/', PaintBudgetCalculatorView.as_view(), name='create-paint-budget'),
]
