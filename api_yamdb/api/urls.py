from django.urls import include, path
from rest_framework import routers

from .views import (CategoriesViewSet, CommentViewSet,
                    GenresViewSet, ReviewViewSet, TitlesViewSet,
                    UserViewSet, get_token, sign_up)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
