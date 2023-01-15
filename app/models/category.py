from django.db import models
from .user import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, related_name="categories", on_delete=models.CASCADE)
    date = models.DateField(blank=True)
    budget = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    is_deleted = models.BooleanField(default=False)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.name