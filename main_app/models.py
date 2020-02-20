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
    # user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def post_relevent():
    	return Post.objects.order_by('-updateDate')

    def post_query(query):
        print(query)

        # Note!!!! Will not return a filtered querySet of both
        filtered_posts = Post.objects.filter(title__icontains = query) | Post.objects.filter(context__icontains = query) | Post.objects.filter(updateDate__icontains = query)

        filtered_posts = filtered_posts.post_relevent()

        # filtered = Post.objects.filter(title__icontains=query, context__icontains=query)
        return filtered_posts


class Comment(models.Model):
    context = models.CharField(max_length = 400)
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.context

###### Error FK referencing for two FK's that point to the same model
class FollowingUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_id')
    follow_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follow_user_id')

    # def activity_following_users():
    #     activity = Post.objects.select_related('follow_user_id').gets(id = id)
    #     return activity