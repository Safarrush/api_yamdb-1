from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)


class User(AbstractUser):
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
        default='user',
        help_text='Роль'
    )
    confirmation_code = models.CharField(
        blank=True,
        max_length=150,
        editable=False,
        help_text='Код подтвержения',
    )

    @property
    def is_admin(self):
        return (
            self.is_staff or self.role == ADMIN
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
