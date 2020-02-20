from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q

# Create your models here.
class Post(models.Model):
		title = models.CharField(max_length = 140)
		context = models.CharField(max_length = 750)
		date = models.DateTimeField(auto_now_add = True)
		updateDate = models.DateTimeField(auto_now_add = True)
		# image = models.ImageField(uploadto = 'img' default = 'img/none.jpg')
		likes = models.IntegerField(default = 0)
		user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')
		def __str__(self):
			return self.title
		def post_relevent():
			return Post.objects.order_by('-updateDate')
		def post_query(self, query):
			return Post.objects.filter(Q(title__icontains='%{query}%')|Q(context__icontains='%{query}%'))

class Comment(models.Model):
    context = models.CharField(max_length = 400)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.context

class Comment(models.Model):
    context = models.CharField(max_length = 400)
    date = models.DateField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='comments')

    def __str__(self):
        return self.context
