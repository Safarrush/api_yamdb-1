from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
        RegexValidator(regex=r'[^\w.@+-]+\z')
        ],
        help_text='Логин'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        help_text='Электронная почта'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        help_text='Фамилия'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        help_text='Имя'
    )
    bio = models.TextField(
        blank=True,
        help_text='Биография'
    )
    role = models.TextField(
        choices=ROLE,
        default='user',
        help_text='Роль'
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=150,
        editable=False,
        unique=True,
        help_text='Код подтвержения',
    )


    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username