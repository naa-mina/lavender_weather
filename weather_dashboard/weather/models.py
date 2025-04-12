from django.db import models
from django.contrib.auth.models import User


class FavoriteCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.user.username}"

