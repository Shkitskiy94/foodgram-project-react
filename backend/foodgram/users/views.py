from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from rest_framework.response import Response
from rest_framework.views import APIView

from djoser.views import UserViewSet

from .models import User, Subscriber
from .serializers import SubscriberSerializer, CustomUserSerializer
from api.pagination import CustomPageNumberPagination


class CustomUserViewSet(UserViewSet):
    """Отображение кастомного юзера"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SubscribeListView(ListAPIView):
    """Отображение списка подписчиков"""
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(author_sub__user=self.request.user)


class SubscribeViewSet(APIView):
    """Отображение конкретного подписчика"""
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscriber.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'вы уже подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscriber.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscriber.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )