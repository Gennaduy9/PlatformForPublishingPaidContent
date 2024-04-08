from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=35, unique=True, verbose_name='номер телефона', **NULLABLE)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата присоединения')
    is_active = models.BooleanField(default=False, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    is_verified = models.BooleanField(default=False, verbose_name='Проверено')

    objects = UserManager()

    # Смена авторизации с имени пользователя на телефонный номер
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('username', 'email', 'phone_number')
