from django.urls import path, include
from rest_framework import routers
from .views import MealViewSet, RatingViewSet

router = routers.DefaultRouter()
router.register(r'meals', MealViewSet, basename='meal')
router.register(r'ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]