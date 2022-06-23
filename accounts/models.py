import email
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name="username")
    email = models.EmailField(max_length=254)


#class FriendShip(models.Model):
#    pass
