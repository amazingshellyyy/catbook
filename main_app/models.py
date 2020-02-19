from django.db import models
from django.utils import timezone
from django.db.models import Q

# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length = 100)
	context = models.CharField(max_length = 200)
	photo_url = models.TextField()
	likes = models.IntegerField(default = 0)
	dateCreated = models.TimeField(auto_now_add=True)
	dateUpdated = models.TimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def post_relevent(self):
		return Post.objects.order_by('-dateUpdated')

	def post_query(self, query):
		return Post.objects.filter(Q(title__icontains='%{query}%')|Q(context__icontains='%{query}%'))

class Comment(models.Model):
	context = models.CharField(max_length = 200)
	post_fk = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return self.context

	# def update_post(self):

