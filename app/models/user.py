from django.db import models
from django.contrib.auth.models import AbstractUser
from ..managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username
