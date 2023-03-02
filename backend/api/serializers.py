from drf_extra_fields.fields import Base64ImageField
from recipe.models import (Basket, Favorite, Ingredient, IngredientQuantity,
                           Recipe, Tag)
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from django.db import transaction


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer для ингедиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Serializer для количества ингредиентов"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Serializer для тэгов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'colour', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer списка рецептов"""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
        
    def get_ingredients(self, obj):
        return IngredientQuantitySerializer(obj.recipe.all(), many=True).data
    
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Basket.objects.filter(user=request.user, recipe=obj).exists()
    
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time', 'pub_date')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Вспомогательный сериализатор рецептов"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientQuantity
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer для рецептов"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = AddIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    
    def validate(self, data):
        ingredients = data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Необходимо выбрать хотя бы 1 ингредиент'
            })
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if not ingredient_id:
                raise serializers.ValidationError({
                    'id': 'Необходимо выбрать хотя бы 1 ингредиент'
                })
            if ingredient_id in ingredients_list:
                raise serializers.ValidationError({
                    'ingredients': 'Все ингредиенты должны быть уникальными'
                })
            ingredients_list.append(ingredient_id)
        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Необходимо выбрать хотя бы 1 тэг'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError({
                    'tags': 'Тэги должны быть уникальными'
                })
            tags_list.append(tag)
        return data
    
    @staticmethod
    def _create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe, ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)
    
    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        if not tags:
            return KeyError('отсутствует тэг')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self._create_ingredients(ingredients, recipe)
        return recipe
    
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data
    
    @transaction.atomic
    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientQuantity.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time')


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class BasketSerializer(serializers.ModelSerializer):
    """Serializer для корзины"""
   
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
    
    class Meta:
        model = Basket
        fields = ('user', 'recipe')


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранных рецептов"""

    def validate(self, data):
        request = self.context.get('request')
        recipe = data['recipe']
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise serializers.ValidationError({
                'status': 'рецепт уже есть в избранном'
            })
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context).data
    
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
