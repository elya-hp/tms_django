from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices


class User(AbstractUser):
    class UserType(TextChoices):
        DRIVER = "driver"
        DISPATCHER = "dispatcher"

    user_type = models.CharField(max_length=100, choices=UserType, null=True)


# TODO: check smth
