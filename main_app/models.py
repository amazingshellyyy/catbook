from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 140)
    context = models.CharField(max_length = 750)
    date = models.DateField()
    image = models.ImageField(uploadto = 'img' default = 'img/none.jpg')
    likes = models.IntegerField(default = 0)
    # user = models.ForeignKey(User, on_delete = models.CASCADE, related, related_name = 'Post')

    def __str__(self):
        return self.title
