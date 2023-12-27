from django.urls import path, include
from rest_framework import routers
from .views import MealViewSet, RatingViewSet

router = routers.DefaultRouter()
router.register(r'meals', MealViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]