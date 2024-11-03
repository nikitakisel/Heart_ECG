from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from user.managers import UserProfileManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=150, unique=True)
    first_name = models.CharField(
        'имя',
        max_length=100,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        'фамилия',
        max_length=100,
        null=True,
        blank=True,
    )
    patronymic = models.CharField(
        'отчество',
        max_length=100,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        'электронная почта',
        null=True,
        blank=True,
        unique=True,
    )
    is_active = models.BooleanField(
        'активен',
        default=False,
    )
    is_staff = models.BooleanField(
        'сотрудник',
        default=False,
    )
    is_superuser = models.BooleanField(
        'суперпользователь',
        default=False,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserProfileManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def natural_key(self):
        return self.username
