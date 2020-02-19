from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = ('title', 'context', 'date', 'likes')
        fields = ('title', 'context', 'likes')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        # fields = ('context', 'date')
        fields = ('context',)

class SearchForm(forms.Form):
	query = forms.CharField(label="Search", max_length=64)