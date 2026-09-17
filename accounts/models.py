from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(null=False,blank=False,unique=True)
    phone = models.CharField(max_length=15,unique=True)
    profile = models.ImageField(upload_to="profiles",null=True,blank=True)
    role = models.CharField(default="customer",max_length=100)
   