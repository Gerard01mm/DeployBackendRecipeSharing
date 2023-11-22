from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# User model
class CustomUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=100, default='')
    list_favorite_recipes = models.JSONField(default=dict)
    list_favorite_ingredients = models.JSONField(default=dict)
    list_favorite_recipe_types = models.JSONField(default=dict)
    list_allergens = models.JSONField(default=dict)
    list_own_recipes = models.JSONField(default=dict)

    def __str__(self):
        return self.username

    def toJson(self):
        return {
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'list_favorite_recipes': self.list_favorite_recipes,
            'list_favorite_ingredients': self.list_favorite_ingredients,
            'list_favorite_recipe_types': self.list_favorite_recipe_types,
            'list_allergens': self.list_allergens,
            'list_own_recipes': self.list_own_recipes,

        }


class Profile(User):
    # create a filed to store a list of integer values named favorite_list
    favorite_list = models.JSONField(default=dict)

    def __str__(self):
        return self.username

    def toJson(self):
        return {
            'username': self.username,
            'email': self.email,
            'favorite_list': self.favorite_list
        }


# Recipe model
class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)

    # create a foreign key to the user model
    ingredients = models.TextField()
    instructions = models.TextField()
    preparation_time = models.IntegerField(default=0)
    servings = models.IntegerField(default=0)
    kcal = models.IntegerField(default=0)
    recipe_type = models.TextField()
    allergens = models.TextField()

    # username_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    username_id = models.TextField()
    creation_date = models.DateField(default=timezone.now)
    # Rating fileds
    rating_average = models.FloatField(default=0.0)
    rating_amount = models.IntegerField(default=0)
    rating_list = models.JSONField(default=dict)
    # Comments fields
    comments_list = models.JSONField(default=dict)
    comments_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'preparation_time': self.preparation_time,
            'servings': self.servings,
            'kcal': self.kcal,
            'recipe_type': self.recipe_type,
            'allergens': self.allergens,
            'username_id': self.username_id,
            'creation_date': self.creation_date.strftime('%Y-%m-%d'),
            'rating_average': str(self.rating_average),
            'rating_amount': self.rating_amount,
            'rating_list': self.rating_list,
            'comments_list': self.comments_list,
            'comments_amount': self.comments_amount
        }
