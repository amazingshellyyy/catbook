from django.contrib import admin
from .models import Post, Comment, UserLikesPost, FollowingUser

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserLikesPost)
admin.site.register(FollowingUser)
