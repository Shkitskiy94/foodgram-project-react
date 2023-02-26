from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SubscribeListView, SubscribeViewSet, CustomUserViewSet)


router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

userpatterns = [
    path(
        'subscriptions/',
        SubscribeListView.as_view(),
        name='subscriptions'
    ),
    path(
        '<int:user_id>/subscribe/',
        SubscribeViewSet.as_view(),
        name='subscribe'
    ),
]

urlpatterns = [
    path('users/', include(userpatterns)),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
