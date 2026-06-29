from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    instagram = models.CharField(max_length=30, blank=True, null=True)
    twitter = models.CharField(max_length=30, blank=True, null=True)
    web_site = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
