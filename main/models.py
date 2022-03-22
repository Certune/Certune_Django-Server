from django.conf import settings
from django.db import models


# Create your models here.
class fileUpload(models.Model):
    name = models.AutoField(primary_key=True)
    audioFile = models.FileField(upload_to='media/')

    def __str__(self):
        # return f"Custom Post object ({self.id})"
        return str(self.name)