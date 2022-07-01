from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(max_length=254)


class Profile(models.Model):
    GENDER_CHOICES = (
        (1, 'Man'),
        (2, 'Woman'),
        (3, 'other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER_CHOICES, verbose_name='gender')
    selfIntro = models.CharField(blank=True, null=True, max_length=252, verbose_name='selfIntro')

# class FriendShip(models.Model):
#    pass


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.username = instance.email
        profile_obj.save()


post_save.connect(post_user_created, sender=User)
