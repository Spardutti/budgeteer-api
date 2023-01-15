from django.db import models
from .category import Category

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    description = models.TextField(blank=True, null=True, max_length=255)
    date = models.DateField(blank=True, null=True) 
