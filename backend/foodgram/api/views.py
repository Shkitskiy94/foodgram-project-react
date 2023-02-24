from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse

from recipe.models import (Basket, Favorite, Ingredient, IngredientQuantity,
                           Recipe, Tag)
from rest_framework import viewsets

from .serializers import (IngredientSerializer, TagSerializer,
                          RecipeListSerializer, RecipeSerializer, BasketSerializer,
                          FavoriteSerializer)
from .permissions import  AuthorOrReadOnly
from .pagination import CustomPageNumberPagination, NoPagination
from .filters import IngredientSearchFilter, RecipeFilter
from foodgram.settings import FILENAME





class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """View представления ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    pagination_class = NoPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """View представления тэгов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = NoPagination


class RecipeViewSet(viewsets.ModelViewSet):
    """View представления рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer
    
    def post_method_actions(self, request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete_method_actions(self, request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_object = get_object_or_404(model, user=user, recipe=recipe)
        model_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_actions(
            request=request, pk=pk, serializers=FavoriteSerializer
        )

    @action(detail=True, methods=["DELETE"],
            permission_classes=[IsAuthenticated])
    def delete_favorite(self, request, pk):
        return self.delete_method_actions(
            request=request, pk=pk, model=Favorite
        )
    
    @action(detail=True, methods=["POST"],
            permission_classes=[IsAuthenticated])
    def shoping_cart(self, request, pk):
        return self.post_method_actions(
            request=request, pk=pk, serializers=BasketSerializer
        )

    @action(detail=True, methods=["DELETE"],
            permission_classes=[IsAuthenticated])
    def delete_shoping_cart(self, request, pk):
        return self.delete_method_actions(
            request=request, pk=pk, model=Basket
        )
    
    @action(
        detail=False,
        methods=["GET"],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        pagination_class=None,
        permission_classes=[IsAuthenticated]
    )
    def download_basket(self, request):
        ingredients = IngredientQuantity.objects.filter(
            recipe__cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total=Sum('quantity'))
        result = 'Cписок покупок:\n\nНазвание продукта - Кол-во/Ед.изм.\n'
        for ingredient in ingredients:
            result += ''.join([
                f'{ingredient["ingredient__name"]} - {ingredient["total"]}/'
                f'{ingredient["ingredient__measurement_unit"]} \n'
            ])
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={FILENAME}'
        return response
