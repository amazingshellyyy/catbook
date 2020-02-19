from django.shortcuts import render
from django.http import HttpResponse
from .models import Post, Comment
from .forms import SearchForm
# Create your views here.
def index(request):
	return HttpResponse('<h1>Catbook</h1>')

def global_view(request):
	# if request.method == 'POST':
	# 	form = SearchForm(request.POST)
	# 	if form.is_valid():
	# 		q = form.cleaned_data['query']
	# 		posts = Post.objects.raw('SELECT * from Post where title likes "%{q}%"')
	# 		return render(request, 'global_view', {'posts': posts})
	form = SearchForm()
	posts = Post.post_relevent(Post.objects.all())
	for post in posts:
		print(post)
		print(post.dateCreated)
	return render(request, 'global_view.html', {'posts': posts, 'form': form})