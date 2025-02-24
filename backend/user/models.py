from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from user.managers import UserProfileManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
    )
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
    sex = models.CharField(
        'пол',
        choices=[('m', 'мужской'), ('w', 'женский')],
        max_length=10,
        default='m',
    )
    date_of_birth = models.DateField(
        'дата рождения',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        'активен',
        default=False,
    )
    is_staff = models.BooleanField(
        'сотрудник',
        default=False,
    )
    is_nurse = models.BooleanField(
        'средний медперсонал',
        default=False,
    )
    is_doctor = models.BooleanField(
        'врач',
        default=False,
    )
    is_superuser = models.BooleanField(
        'суперпользователь',
        default=False,
    )

    profile_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    profile_id = models.PositiveIntegerField(null=True, blank=True)
    profile = GenericForeignKey('profile_type', 'profile_id')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserProfileManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def natural_key(self):
        return self.username


class Profile(models.Model):
    class Meta:
        abstract = True


class PacienteProfile(Profile):
    class Meta:
        verbose_name = 'профиль пациента'
        verbose_name_plural = 'профили пациентов'

    weight = models.PositiveIntegerField(
        'вес',
        null=True,
        blank=True,
    )
    systolic_blood_pressure = models.PositiveIntegerField(
        'систолическое артериальное давление',
        null=True,
        blank=True,
    )
    diastolic_blood_pressure = models.PositiveIntegerField(
        'диастолическое артериальное давление',
        null=True,
        blank=True,
    )
    health_status = models.TextField(
        'состояние',
        null=True,
        blank=True,
    )
    skin_and_mucous_membrane = models.TextField(
        'кожа и слизистая оболочка',
        null=True,
        blank=True,
    )
    subcutaneous_fat = models.TextField(
        'подкожно-жировая клетчатка',
        null=True,
        blank=True,
    )
    lymphatic_system = models.TextField(
        'лимфатическая система',
        null=True,
        blank=True,
    )
    musculoskeletal_system = models.TextField(
        'опорно-двигательная система',
        null=True,
        blank=True,
    )
    respiratory_system = models.TextField(
        'дыхательная система',
        null=True,
        blank=True,
    )
    cardiovascular_system = models.TextField(
        'сердечно-сосудистая система',
        null=True,
        blank=True,
    )
    digestive_system = models.TextField(
        'пищеварительная система',
        null=True,
        blank=True,
    )
    genitourinary_system = models.TextField(
        'мочеполовая система',
        null=True,
        blank=True,
    )
    endocrine_system = models.TextField(
        'эндокринная система',
        null=True,
        blank=True,
    )
    nervous_system = models.TextField(
        'нервная система',
        null=True,
        blank=True,
    )
    past_illnesses = models.TextField(
        'перенесенные заболевания',
        null=True,
        blank=True,
    )
    disability = models.BooleanField(
        'инвалидность',
        default=False,
    )
    education = models.CharField(
        'образование',
        max_length=200,
        null=True,
        blank=True,
    )
    profession = models.CharField(
        'профессия',
        max_length=100,
        null=True,
        blank=True,
    )
    family_status = models.CharField(
        'семейный статус',
        choices=[
            ('married', 'женат'),
            ('not_married', 'не женат'),
        ],
        max_length=11,
        null=True,
        blank=True,
    )
    has_children = models.BooleanField(
        'есть дети',
        default=False,
    )


class PersonalProfile(Profile):
    class Meta:
        verbose_name = 'профиль персонала'
        verbose_name_plural = 'профили персонала'

    institution = models.CharField(
        'ЛПУ',
        max_length=150,
        null=True,
        blank=True,
    )
    subdivision = models.CharField(
        'подразделение',
        max_length=150,
        null=True,
        blank=True,
    )
