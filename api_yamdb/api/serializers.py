from django.core.validators import RegexValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import ROLE, User


class UserViewSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.CharField(max_length=254)
    role = serializers.ChoiceField(
        choices=ROLE,
        default='user',
        required=False
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        model = User

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя недоступно!'
            )
        if User.objects.filter(
            username=username
        ).exists():
            raise serializers.ValidationError(
                'Такое имя уже зарегистрироавно!'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такая почта уже зарегистрирована!'
            )
        return email


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')],
        max_length=150
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя недоступно!'
            )
        return username


class AuthenticatedSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class TitleReadSerializer(TitleSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title',
        )

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Отзыв на это произведение у вас уже есть',
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        model = Comment
