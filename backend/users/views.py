from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import CustomUser
from rest_framework.decorators import action
from rest_framework import status
from .pagination import CustomUserPagination
from users.models import Follow
from api.permissions import OnlyAuthorOrStaff
from api.serializers import CustomUserSerializer, CustomUserCreateSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomUserPagination
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='me',
            permission_classes=[OnlyAuthorOrStaff])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.user.is_authenticated:
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'detail': 'Учетные данные не были предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED)

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer
        return CustomUserSerializer

    @action(detail=False, methods=['get'], url_path='subscriptions',
            permission_classes=[OnlyAuthorOrStaff])
    def subscriptions(self, request):
        subscriptions = request.user.follower.all()
        page = self.paginate_queryset(subscriptions)
        serializer = CustomUserSerializer(page,
                                          many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post',
                     'delete'],
            url_name='subscribe',
            url_path='subscribe',
            permission_classes=[IsAuthenticated])
    def subscribe_or_unsubscribe(self, request, pk=None):
        current_user = request.user
        user_to_manage = self.get_object()
        if current_user == user_to_manage:
            return Response({'detail': 'You cannot subscribe'
                             'to yourself.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            follow, created = Follow.objects.get_or_create(user=user_to_manage,
                                                           author=current_user)
            if created:
                return Response({'detail': 'Successfully subscribed'
                                 'to the user.'}, status=status.HTTP_201_CREATED)
            return Response({'detail': 'You are already subscribed'
                             'to this user.'}, status=status.HTTP_200_OK)

        follow = get_object_or_404(Follow, user=user_to_manage,
                                   author=current_user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
