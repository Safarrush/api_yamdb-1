from django.db import models

from .validators import validate_year


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Cтрока идентификатор'
    )

    def __str__(self):
        return f'Категория: {self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Cтрока идентификатор'
    )

    def __str__(self):
        return f'Жанр: {self.name}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='Описание произведения',
    )
    genre = models.ForeignKey(
        Genres,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )
    categories = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория произведения',
    )

    def __str__(self):
        return (f'Произведение - {self.name}, '
                f'является {self.categories} '
                f'и относится к жанру {self.genre}.')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
