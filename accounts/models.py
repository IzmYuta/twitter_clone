import email
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(max_length=254)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, verbose_name="username")
    email = models.EmailField(max_length=254)


# class FriendShip(models.Model):
#    pass


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.username = instance.email
        profile_obj.save()


post_save.connect(post_user_created, sender=User)
