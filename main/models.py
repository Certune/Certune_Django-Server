from django.db import models


# Create your models here.
class Song(models.Model):
    userEmail = models.CharField(max_length=100)
    songName = models.CharField(max_length=100)
