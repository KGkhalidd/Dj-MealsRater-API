from django.contrib import admin
from .models import Meal, Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal', 'user', 'stars', 'created')
    list_filter = ('meal', 'user', 'stars')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created')
    list_filter = ('title', 'description')
    search_fields = ('title', 'description')
