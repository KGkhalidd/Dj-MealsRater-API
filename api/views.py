from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def meal_rater(self, request, pk=None):
        if 'stars' in request.data:
            '''
            create or update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            # username = request.data['username']
            # user = User.objects.get(username=username)
            
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    # override update method to prevent update of rating by user by sending bad request
    def update(self, request, *args, **kwargs):
        response = {'message': 'you cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    # override create method to prevent creation of rating by user by sending bad request
    def create(self, request, *args, **kwargs):
        response = {'message': 'you cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


