from django.db import models
from django.contrib.auth.models import User
from .mealrating import MealRating



class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, related_name="mealfavorites")
        
    
    
    # @property
    # def user_rating(self, request):
    #     """user rating """
    #     user_rating = MealRating.objects.filter(meal=self).filter(user=request.auth.user)
        
    #     return user_rating
    
    # @property
    # def user_rating(self):
    #     """user rating """
    #     return self.user_rating
    
    # @user_rating.setter
    # def user_rating(self, value):
    #     self.__user_rating = value
    
    # @property
    # def user_rating(self):
    #     ratings = MealRating.objects.filter(meal=self)

        

    @property
    def avg_rating(self):
        """avg rating calculated attribute for each meal"""
        ratings = MealRating.objects.filter(meal=self)

        # Sum all of the ratings for the meal
        total_rating = 0
        if len(ratings) > 0:
            for rating in ratings:
                total_rating += rating.rating
            avg_rating = total_rating / len(ratings)
            return avg_rating
    

    # TODO: Add an user_rating custom properties

    # TODO: Add an avg_rating custom properties
