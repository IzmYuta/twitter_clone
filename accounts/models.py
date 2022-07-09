from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(max_length=254)


class Profile(models.Model):
    GENDER = (
        (1, "Man"),
        (2, "Woman"),
        (3, "other"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.IntegerField(
        blank=True, null=True, choices=GENDER, verbose_name="gender"
    )
    self_intro = models.CharField(
        blank=True, null=True, max_length=252, verbose_name="self_intro"
    )


class FriendShip(models.Model):
    followee = models.ForeignKey(
        User, related_name="follower", on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        User, related_name="followee", on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["followee", "follower"], name="follow_unique"
            ),
        ]


@receiver(post_save, sender=User)
def post_user_created(sender, instance, created, **kwargs):
    if created:
        profile_obj = Profile(user=instance)
        profile_obj.save()
