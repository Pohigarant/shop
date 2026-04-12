from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Электронная почта")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Номер мобильного телефона")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username
