from django.shortcuts import render
from users.models import User
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def users_profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    