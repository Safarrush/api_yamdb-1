from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import ROLE, User
from titles.models import Categories, Genres, Titles


class UserViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False, default='user')

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        lookup_field = ('username')

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError('Нельзя использовать это имя!')
        elif not name or name == "":
            raise serializers.ValidationError('Это поле обязательно!')
        return name

    def validate_email(self, email):
        if not email or email == "":
            raise serializers.ValidationError('Это поле обязательно!')
        return email


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

    class Meta:
        fields = ('email', 'username')
        model = User
        read_only_fields = ('confirmation_code',)

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError('Нельзя использовать это имя!')
        return name

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
                User.objects.filter(username=username).exists()
                and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError('Такое имя уже существует!')
        if (
                User.objects.filter(email=email).exists()
                and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError('Такая почта уже существует!')
        return data


class AuthenticatedSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True, max_length=255)

    class Meta:
        model = User
        fields = (
            'username', 'confirmation_code'
        )

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError('Это поле обязательно!')
        if confirmation_code is None:
            raise serializers.ValidationError('Это поле обязательно!')
        return data


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Titles
