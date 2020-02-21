from django.db import models
from main_app.models import Post
# Create your models here.

class Image(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()