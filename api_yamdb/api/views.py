from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (SAFE_METHODS, AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api.filters import TitleFilter
from api.permissions import (AdminModeratorAuthorOrReadOnly, IsAdmin,
                          IsAdminOrReadOnlyPermission)
from api.serializers import (AuthenticatedSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, MeSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserViewSerializer)
from api.utils import BaseCategoryGenreViewSet, BaseUserTitleReviewCommentViewSet


class UserViewSet(BaseUserTitleReviewCommentViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserViewSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdmin,)

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=MeSerializer
    )
    def users_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_meil(user):
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        subject='Регистрация',
        message=f'Код подтверждения: {user.confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes((AllowAny,))
def sign_up(request):
    check_user = User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    )
    if check_user:
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    send_meil(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = AuthenticatedSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'})
        else:
            return Response(
                'Не подходит токен!',
                status=status.HTTP_400_BAD_REQUEST
            )
    return Response(
        'Проблема с аутентификацей!',
        status=status.HTTP_400_BAD_REQUEST
    )


class CategoryViewSet(BaseCategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnlyPermission,
    )


class GenreViewSet(BaseCategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnlyPermission,
    )


class TitleViewSet(BaseUserTitleReviewCommentViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnlyPermission,
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(BaseUserTitleReviewCommentViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AdminModeratorAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()


class CommentViewSet(BaseUserTitleReviewCommentViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        AdminModeratorAuthorOrReadOnly
    )

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review = Review.objects.filter(title_id=title_id)
        return get_object_or_404(review, id=self.kwargs.get('review_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        review=self.get_review()
        return review.comments.all()
