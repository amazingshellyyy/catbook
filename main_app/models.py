from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 140)
    context = models.CharField(max_length = 750)
    date = models.DateField()
    # image = models.ImageField(uploadto = 'img' default = 'img/none.jpg')
    likes = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    context = models.CharField(max_length = 400)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments')
    def __str__(self):
        return self.context