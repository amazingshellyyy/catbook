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
    likes = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')

    def __str__(self):
        return self.title

    def post_relevent():
        return Post.objects.order_by('-updateDate')

    def post_query(query):
        print(query)

        # Note!!!! Will not return a filtered querySet of both
        filtered_posts = (Post.objects.filter(title__icontains = query) | Post.objects.filter(context__icontains = query) | Post.objects.filter(updateDate__icontains = query)).order_by('-updateDate') 

        # filtered = Post.objects.filter(title__icontains=query, context__icontains=query)
        return filtered_posts


class Comment(models.Model):
    context = models.CharField(max_length = 400)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.context

class FollowingUser(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_id')
    follow_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follow_user_id')

    def activity_following_users(id):
        user = User.objects.get(id = id)

        activity = Post.objects.raw("select * from main_app_post left outer join main_app_followinguser on (main_app_post.user_id = main_app_followinguser.follow_user_id_id) where main_app_followinguser.user_id_id =" + str(id))

        [print(a) for a in activity]
        return activity

class UserLikesPost(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)