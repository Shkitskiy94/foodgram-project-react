from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscriber, User

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'username',
    )


@admin.register(Subscriber)
class SubcribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    list_filter = (
        'author',
    )