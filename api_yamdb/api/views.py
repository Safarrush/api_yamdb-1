from django.shortcuts import render
from users.models import User
from rest_framework import filters, mixins, permissions, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdmin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.decorators import action, api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    UserViewSerializer,
    SignUpSerializer,
    AuthenticatedSerializer,
    TitlesSerializer,
    CategoriesSerializer,
    GenresSerializer,
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from titles.models import Categories, Genres, Titles

EMAIL = f'from@yandex.ru'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserViewSerializer
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


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация',
            message=f'Код подтверждения: {confirmation_code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = AuthenticatedSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
