"""View module for handling requests about restaurants"""
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from favamealapi.models import Restaurant
from django.contrib.auth.models import User

class FaveSerializer(serializers.ModelSerializer):
    """JSON serializer for users in favorites"""
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username',)
        
class RestaurantSerializer(serializers.ModelSerializer):
    """JSON serializer for restaurants"""
    favorites = FaveSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'address', 'favorites',)
        depth = 1
        
        
        
        
class RestaurantView(ViewSet):
    """ViewSet for handling restuarant requests"""
    
    def list(self, request):
        """Handle GET requests to restaurants resource

        Returns:
            Response -- JSON serialized list of restaurants
        """
        restaurants = Restaurant.objects.all()


        serializer = RestaurantSerializer(restaurants, many=True, context={'request': request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            restaurant = Restaurant.objects.get(pk=pk)

            serializer = RestaurantSerializer(
                restaurant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
    def create(self, request):
        """Handle POST operations for restaurants

        Returns:
            Response -- JSON serialized event instance
        """
        rest = Restaurant()
        rest.name = request.data["name"]
        rest.address = request.data["address"]

        try:
            rest.save()
            serializer = RestaurantSerializer(
                rest, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: Write a custom action named `star` that will allow a client to
    # send a POST and a DELETE request to /restaurant/2/star