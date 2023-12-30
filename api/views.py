from django.shortcuts import render
from rest_framework import viewsets
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer, UserSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import  IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    # made override cause we used AllowAny permission class
    # override create method to create token for user
    def create(self, request, *args, **kwargs):
        # takes the data from the request and passes it to the serializer
        serializer = self.get_serializer(data=request.data)
        # checks if the data is valid
        serializer.is_valid(raise_exception=True)
        # saves the data in the database
        self.perform_create(serializer)
        # creates token for the user
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key,}, status=status.HTTP_201_CREATED)


    # override list method to prevent listing of users 
    def list(self, request, *args, **kwargs):
        response = {'message': 'you cant list users like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    # override destroy method to prevent deletion of users
    def destroy(self, request, *args, **kwargs):
        response = {'message': 'you cant delete users like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    # override retrieve method to prevent retrieval of users
    def retrieve(self, request, *args, **kwargs):
        response = {'message': 'you cant retrieve users like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    # override update method to prevent update of users
    def update(self, request, *args, **kwargs):
        response = {'message': 'you cant update users like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
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


