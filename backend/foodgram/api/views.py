from rest_framework import viewsets

from recipe.models import (Ingredient, Recipe, Tag, IngredientQuantity,
                           Basket, Favorite)
from users.models import User, Subscriber
from .serializers import (UserSerializer, SubscriberSerializer,
                          IngredientSerializer, )



class UserViewSet(viewsets.ModelViewSet):
    """View представления пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    """View представления подписчиков"""
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """View представления ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

