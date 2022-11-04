from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    amount = models.IntegerField(default=0)
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class WeeklyCategory(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, related_name="categories", on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class WeeklyExpense(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    weekly_category = models.ForeignKey(WeeklyCategory, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    

class MonthlyIncome(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
