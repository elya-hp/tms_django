from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db import models


class DispatcherManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=get_user_model().UserType.DISPATCHER)


class DriverManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type=get_user_model().UserType.DRIVER)


class DriverQuerySet(models.QuerySet):
    ...


class DispatcherQuerySet(models.QuerySet):
    ...
