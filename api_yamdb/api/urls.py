from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, sign_up, get_token

app_name = 'api'

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
]