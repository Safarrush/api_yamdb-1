from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import validate_year
from users.models import User

LEN_NAME = settings.MAX_LEN_NAME
LEN_SLUG = settings.MAX_LEN_SLUG


class Category(models.Model):
    name = models.CharField(
        max_length=LEN_NAME,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=LEN_SLUG,
        unique=True,
        verbose_name='Слаг категории',
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=LEN_NAME,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=LEN_SLUG,
        unique=True,
        verbose_name='Псевдоним жанра',
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год написания',
        validators=(validate_year,),
        db_index=True,
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review',
            ),
        )

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
