from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Form
from .forms import PostForm, CommentForm

# Create your views here.
def index(request):
	return HttpResponse('<h1>Catbook</h1>')

# -------- Post views -------- #
def post_list(request):
	posts = Post.objects.all()
	return render(request, 'post_list.html', {'posts' : posts})

def post_detail(request, pk):
	post = Post.objects.get(id = pk)
	return render(request, 'post_detail.html', {'post' : post})

def post_create(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save()
			return redirect('comment_detail', pk = comment.pk)

	else:
		form = PostForm(instance = post)
	return render(request, 'post_form.html', {'form' : form})

def post_delete(request, pk):
	Post.objects.get(id = pk).delete()
	return redirect('comment_list')