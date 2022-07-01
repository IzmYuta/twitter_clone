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
    username = models.CharField(max_length=150, verbose_name='username')
    email = models.EmailField(max_length=254)
    gender = models.IntegerField(blank=True, null=True, choices=GENDER_CHOICES, verbose_name='gender')
    selfIntro = models.CharField(blank=True, null=True, max_length=252, verbose_name='selfIntro')

# class FriendShip(models.Model):
#    pass


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.username = instance.username
        profile_obj.email = instance.email
        profile_obj.save()


post_save.connect(post_user_created, sender=User)


@receiver(post_save, sender=Profile)
def post_profile_changed(sender, instance, created, **kwargs):
    if not created:
        # パスワードが保存されなかった
        user_obj = User(profile=instance)
        user_obj.pk = instance.pk
        user_obj.username = instance.username
        user_obj.email = instance.email
        user_obj.save()


post_save.connect(post_profile_changed, sender=Profile)
