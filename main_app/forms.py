from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'context', 'date', 'image', 'likes')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('context', 'date')