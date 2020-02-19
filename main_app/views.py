from django.shortcuts import render, redirect
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
			return redirect('comment_detail', pk = post.pk)

	else:
		form = PostForm()
	context = {'form' : form, 'header': "Add New Post"}
	return render(request, 'post_form.html', context)

def post_edit(request, pk):
	post = Post.objects.get(pk = pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance = post)
		if form.is_valid():
			post = form.save()
			return redirect('post_detail', pk = post.pk)

	else:
		form = PostForm(instance = post)
	return render(request, 'post_form.html', {'form' : form})

def post_delete(request, pk):
	Post.objects.get(id = pk).delete()
	return redirect('comment_list')

# -------- Comment views -------- #
def comment_list(request):
	comments = Comment.objects.all()
	return render(request, 'comment_list.html', {'comments' : comments})

def comment_detail(request, pk):
	comment = Comment.objects(id = pk)
	return render(request, 'comment_detail.html', {'comment' : comment})

def comment_create(request):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save()
			return redirect('comment_detail', pk = comment.pk)

	else:
		form = CommentForm()
	context = {'form' : form, 'header' : "Add New Comment"}
	return render(request, 'comment_form.html', context)

def comment_edit(request, pk):
	comment = Comment.objects.get(pk = pk)
	if request.method == 'POST':
		form = CommentForm(request.POST, instance = comment)
		if form.is_valid():
			comment = form.save()
			return redirect('comment_detail', pk = comment.pk)

	else:
		form = CommentForm(instance = comment)
	return render(request, 'comment_form.html', {'form' : form})

def comment_delete(request, pk):
	Comment.objects.get(id = pk).delete()
	return redirect('comment_list')