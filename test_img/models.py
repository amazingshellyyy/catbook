from django.db import models
from main_app.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'profileImage')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()
    
    def __str__(self):
        return self.upload.name
    # def get_absolute_url(self):
    #     return reverse('profile', args=[self.user.id])

class ProfileImage(models.Model):
    image_url = models.CharField(max_length=700)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'profile_image')
