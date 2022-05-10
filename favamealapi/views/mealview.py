"""View module for handling requests about meals"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from favamealapi.models import Meal, Restaurant
from favamealapi.models.mealrating import MealRating
from favamealapi.views.restaurantview import FaveSerializer

class MealRatingSerializer(serializers.ModelSerializer):
    """JSON serializer for Meal Rating"""
    
    class Meta:
        model = MealRating
        fields = ('id', 'rating',)
        depth = 1

class NestedRestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', )
        depth = 1

class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = NestedRestaurantSerializer(many=False)
    favorites = FaveSerializer(many=True)
    # mealrating = MealRatingSerializer(many=True)
    
    
    class Meta:
        model = Meal
        fields = ('id', 'name', 'restaurant', 'favorites', 'avg_rating', )
        depth = 1
    
class MealView(ViewSet):
    """ViewSet for handling meal requests"""
    
    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.all()
        
        for meal in meals:
            # get mealratings matching meal
            mealratings = MealRating.objects.filter(meal=meal)
            # get current user
            user = request.user
            # if currentuser = mealratings_user
            usermealratings = mealratings.get(user_id=user)
            meal.user_rating = usermealratings

        serializer = MealSerializer(meals, many=True, context={'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.get(pk=pk)

            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        meal = Meal()
        meal.name = request.data["name"]
        meal.restaurant = Restaurant.objects.get(pk=request.data["restaurant_id"])

        try:
            meal.save()
            serializer = MealSerializer(
                meal, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)