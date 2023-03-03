from django.contrib import admin
from django.contrib.admin import display

from .models import (Ingredient, Recipe, Tag, IngredientQuantity,
                    Basket, Favorite)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientQuantity
    min_num = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'added_in_favorites'
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )

    search_fields = ('name',)
    inlines = [IngredientAmountInline]

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorite.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
    )


@admin.register(IngredientQuantity)
class IngredientQuantityAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = (
        'recipe',
    )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
    )