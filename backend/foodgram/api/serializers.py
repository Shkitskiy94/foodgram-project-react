from rest_framework.serializers import ModelSerializer
from recipe.models import (Ingredient, Recipe, Tag, IngredientQuantity,
                           Basket, Favorite)
from users.models import User, Subscriber


class UserSerializer(ModelSerializer):
    """Serializer для пользователя"""
    class Meta:
        abstract = True
        model = User
        fields = ('email', 'username','first_name', 'last_name')


class SubscriberSerializer(ModelSerializer):
    """Serializer для подписчика"""
    class Meta:
        model = Subscriber
        fields = ('user', 'author')


class IngredientSerializer(ModelSerializer):
    """Serializer для ингедиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'unit_of_measurement')


class RecipeSerializer(ModelSerializer):
    """Serializer для рецептов"""
    class Meta:
        model = Recipe
        fields = ('author', 'ingredients', 'name', 'image', 'description',
                  'tags', 'cooking_time', 'pub_date')


class TagSerializer(ModelSerializer):
    """Serializer для тэгов"""
    class Meta:
        model = Tag
        fields = ('name', 'colour', 'slug')


class IngredientQuantitySerializer(ModelSerializer):
    """Serializer для тэгов"""
    class Meta:
        model = IngredientQuantity
        fields = ('recipe', 'ingredient', 'quantity')


class BasketSerializer(ModelSerializer):
    """Serializer для корзины"""
    class Meta:
        model = Basket
        fields = ('user', 'recipe')


class FavoriteSerializer(ModelSerializer):
    """Serializer для избранное"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
