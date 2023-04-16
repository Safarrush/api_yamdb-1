from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_year(value):
    if value > timezone.localtime().year:
        raise ValidationError(
            _('%(value) год ещё не наступил, '
              'я сейчас выгляну в окно и не '
              'дай бог я не увижу вашей машины времени'),
            params={'value': value},
        )
