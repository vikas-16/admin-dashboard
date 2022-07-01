from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User  

class Student(models.Model):

    name = models.CharField(max_length=70)
    email = models.CharField(max_length=70)
    password = models.CharField(max_length=70)
  