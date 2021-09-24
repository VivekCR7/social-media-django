from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to = 'profile_pics')
    biography = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print("Profile created!")

post_save.connect(create_profile, sender=User)

def save_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()
        print("Profile updated!")

post_save.connect(save_profile, sender=User)