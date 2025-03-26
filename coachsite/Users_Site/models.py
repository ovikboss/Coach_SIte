from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    height = models.FloatField(blank=True, null=True, verbose_name='Рост (см)')
    weight = models.FloatField(blank=True, null=True, verbose_name='Вес (кг)')
    age = models.IntegerField(blank=True, null=True, verbose_name='Возраст')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    hide_phone_number = models.BooleanField(default=False, verbose_name='Скрыть номер телефона')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="accounts_user_groups",  # Добавляем related_name
        related_query_name="accounts_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="accounts_user_permissions",  # Добавляем related_name
        related_query_name="accounts_user",
    )

    def __str__(self):
        return self.username

