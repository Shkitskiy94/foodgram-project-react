from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Subscriber(models.Model):
    """Модель подписчика"""
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
    )
    
    author = models.ForeignKey(
        User,
        related_name='user',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'