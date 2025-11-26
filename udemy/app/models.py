from django.db import models

# Create your models here.

class Name(models.Model):
    name = models.CharField(max_length=20)