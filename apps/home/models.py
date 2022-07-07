from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User  


class Category(models.Model):
    city = models.CharField(max_length=70 , default="")
    def __str__(self):
        return self.city

class Student(models.Model):
    city = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=70)
