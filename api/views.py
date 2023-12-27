from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(detail=True, methods=['POST'])
    def meal_rater(self, request, pk=None):
        if 'stars' in request.data:
            '''
            create or update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            username = request.data['username']
            user = User.objects.get(username=username)
            
            try:
                # update
                rating = Rating.objects.get(user=user.id, meal= meal.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many = False)
                json ={
                    'message': 'Meal Rate Updated',
                    'result': serializer.data
                }
                return Response(json, status= status.HTTP_200_OK)

            except ObjectDoesNotExist:
                # create
                rating = Rating.objects.create(user= user, meal= meal, stars=stars)
                serializer = RatingSerializer(rating, many = False)
                json ={
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json, status= status.HTTP_201_CREATED)
        
        else:
            json = {
                'message': 'you must provide stars'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)



class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


