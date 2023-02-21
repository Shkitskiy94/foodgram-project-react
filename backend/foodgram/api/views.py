from recipe.models import (Basket, Favorite, Ingredient, IngredientQuantity,
                           Recipe, Tag)
from rest_framework import viewsets
from users.models import Subscriber, User

from .serializers import (BasketSerializer, FavoriteSerializer,
                          IngredientQuantitySerializer, IngredientSerializer,
                          RecipeSerializer, SubscriberSerializer,
                          TagSerializer, UserSerializer)
from .permissions import IsAdminOrReadOnly, AuthorOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """View представления пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriberViewSet(viewsets.ModelViewSet):
    """View представления подписчиков"""
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """View представления ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """View представления рецептов"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly | IsAdminOrReadOnly,)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """View представления тэгов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientQuantityViewSet(viewsets.ModelViewSet):
    """View представления ингредиентов в рецепте"""
    queryset = IngredientQuantity.objects.all()
    serializer_class = IngredientQuantitySerializer


class BasketViewSet(viewsets.ModelViewSet):
    """View представления корзины"""
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    """View представления списка избранных"""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer