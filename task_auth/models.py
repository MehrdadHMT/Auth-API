from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import rest_framework.authtoken.models

from .validators import phone_regex_validator


class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex_validator], unique=True, max_length=11)
    has_valid_phone_number = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["phone_number"]


class Token(rest_framework.authtoken.models.Token):
    """
    key is no longer primary key, but still indexed and unique
    relation to user is a ForeignKey, so each user can have more than one token
    """

    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    user_agent = models.CharField(max_length=255)
