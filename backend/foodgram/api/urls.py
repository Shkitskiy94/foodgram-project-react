from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,)


app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')
v1_router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(v1_router.urls))
]
