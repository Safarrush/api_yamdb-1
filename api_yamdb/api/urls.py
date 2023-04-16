from django.urls import include, path
from rest_framework import routers


from .views import (
    UserViewSet,
    sign_up,
    get_token,
    CategoriesViewSet,
    TitlesViewSet,
    GenresViewSet
)

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register('categories', CategoriesViewSet, basename='categories')
router.register('genres', GenresViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]
