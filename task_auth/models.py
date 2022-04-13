from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_regex_validator = RegexValidator(regex=r"^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$",
                                       message="Phone number must be entered in one of these formats: '09xxxxxxxxx',"
                                               " '989xxxxxxxxx', '+989xxxxxxxxx', '+9809xxxxxxxxx', '00989xxxxxxxxx',"
                                               "'0989xxxxxxxxx', '009809xxxxxxxxx'."
                                               " Up to 15 digits allowed.")


class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex_validator], unique=True, max_length=11)

    REQUIRED_FIELDS = ["phone_number"]


"""
Overriding 'rest_framework.authtoken.models' to be able to use multiple tokens for each user.
"""
import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

import rest_framework.authtoken.models


class Token(rest_framework.authtoken.models.Token):
    # key is no longer primary key, but still indexed and unique
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)
    # relation to user is a ForeignKey, so each user can have more than one token
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='auth_tokens',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    user_agent = models.CharField(max_length=255)
