from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'post_pics')
    caption = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author}'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 600 or img.width > 600:
            output_size = (600,600)
            img.thumbnail(output_size)
            img.save(self.image.path)