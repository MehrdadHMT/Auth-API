from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    phone_number = models.IntegerField(unique=True)

    REQUIRED_FIELDS = ["phone_number"]
