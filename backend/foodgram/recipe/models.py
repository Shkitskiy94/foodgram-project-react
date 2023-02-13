from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        max_length=100,
        verbose_name='название ингедиента'
    )
    unit_of_measurement = models.CharField(
        max_length=20,
        verbose_name='единица измерений',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.unit_of_measurement}'



class Recipe(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='author',
        to=User,
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        related_name='ingredients',
        through='IngredientQuantity',
        to=Ingredient,
        verbose_name='ингредиенты',
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='images/',
        verbose_name='изображение',
    )
    description = models.TextField(verbose_name='описание')
    tags = models.ManyToManyField(
        related_name= 'tags',
        to='Tag',
        verbose_name='тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления',
        validators=[
            MinValueValidator(settings.MIN_COOKING_VALUE),
            MaxValueValidator(settings.MAX_COOKING_VALUE),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=100,
        verbose_name='название тега',

    )
    colour = models.CharField(
        max_length=30,
        verbose_name='цвет',
    )
    slug = models.SlugField(
        unique=True,
        )
    
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipe',
        to='Recipe',
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='ingredient',
        to='Ingredient',
        verbose_name='ингредиент',
    )
    quantity = models.PositiveSmallIntegerField(null=True)

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'



class Basket(models.Model):
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        to=User,
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        to='Recipe',
        verbose_name='рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_basket'
            )
        ]
        verbose_name = 'корзина покупок'
        verbose_name_plural = 'корзина покупок'
    
    def __str__(self):
        return f'{self.user} добавил {self.recipe} в козину покупок'
    
    
class Favorite(models.Model):
    user = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorite',
        to=User,
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='favorite',
        to='Recipe',
        verbose_name='рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
    
    def __str__(self):
        return f'{self.user} добавил {self.recipe} в список избранных'