from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    matricula = models.CharField(max_length=20, blank=True, null=True, verbose_name='Matrícula')
    carrera = models.CharField(max_length=100, blank=True, null=True, verbose_name='Carrera')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.matricula or 'Sin matrícula'})"
