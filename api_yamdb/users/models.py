from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'
MAX_LENGTH = 150

ROLE = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)


class User(AbstractUser):
    username = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        verbose_name="Email", unique=True,
        help_text='Электронная почта'
    )
    bio = models.TextField(
        blank=True,
        help_text='Биография'
    )
    role = models.TextField(
        choices=ROLE,
        default=USER,
        help_text='Роль'
    )

    @property
    def is_admin(self):
        return (
            self.is_staff or self.is_superuser or self.role == ADMIN
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
