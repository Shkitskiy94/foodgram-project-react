from rest_framework import serializers
from djoser.serializers import (
    UserCreateSerializer, UserSerializer
)

from .models import User, Subscriber
from recipe.models import Recipe


class SmallRecipeSerializer(serializers.ModelSerializer):
    """Serializer рецептов"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(UserSerializer):
    """Serializer пользователя"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')
        
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscriber.objects.filter(user=user, author=obj.id).exists()


class SubscriberSerializer(CustomUserSerializer):
    """Serializer подписчика"""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    @staticmethod
    def get_recipes_count(obj):
        return obj.author.count()
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.author.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return SmallRecipeSerializer(recipes, many=True).data
    

class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer создания пользователя"""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'  
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        if not validated_data['email']:
            raise ValueError("укажите email")
        user = User.objects.create(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
