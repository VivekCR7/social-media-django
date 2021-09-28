from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics')
    caption = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    like = models.ManyToManyField(User, related_name='post_like')

    def total_likes(self):
        return self.like.count()

    def __str__(self):
        return f'{self.author}'

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 600 or img.width > 600:
    #         output_size = (600, 600)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True)
    content = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('date_published',)

    def __str__(self):
        return f'Comment by {self.author}'

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
