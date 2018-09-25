from django.urls import path

from .views import ProductPriceViewSet

urlpatterns = [
    path('get-price/', ProductPriceViewSet.as_view()),
]
