from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    last_played = models.DateTimeField(null = True, blank = True)
    user =models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    def __str__(self):
        return self.title