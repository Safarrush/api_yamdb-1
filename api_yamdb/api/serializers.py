from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class UserViewSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=[validate_username],
        max_length=150
    )
    email = serializers.EmailField(max_length=254)


class AuthenticatedSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class MeSerializer(UserViewSerializer):

    class Meta(UserViewSerializer.Meta):
        read_only_fields = ('role',)


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


class BaseTitleSerializer(serializers.ModelSerializer):
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


class TitleReadSerializer(BaseTitleSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(BaseTitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        if self.context.get('request').method != 'POST':
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
