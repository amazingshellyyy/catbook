from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment, UserLikesPost
from .forms import PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from faker import Faker

# *******Fake Data*********
# NOTE: This function is called in on the landing page to create the fake data. If you do not comment it out, you will make a lot of entries
def load_fake():
	default_pass = '1234'
	fake = Faker()

	# ***** Create Fake User ************
	for _ in range(10):
		user = User.objects.create_user(
			username = fake.name(),
			email = fake.email(),
			password = default_pass,
		)
		user.save()

	# ******** Create Fake Posts **********
	for user in User.objects.all():
		post = Post.objects.create(
			title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
			context = fake.text(max_nb_chars=200, ext_word_list= None),
			user = user
			)
		post.save()

	# ********** Create Fake Comments ********
	for post in Post.objects.all():
		comment = Comment.objects.create(
			context = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
			post = post,
			user = post.user
			)
		comment.save()

def is_search_requested(request):
	if request.method == 'POST':
		if 'query' in request.POST.keys():
			return True
		return False
	return False

# Create your views here.
def index(request):
	load_fake()
	# if user search redirect to global view
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	return render(request, 'index.html')

# -------- Post views -------- #
@login_required
def profile(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	user = User.objects.get(pk=pk)
	posts = Post.objects.filter(user=user)
	return render(request, 'profile.html', {'user':user, 'posts' : posts})

def post_detail(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	post = Post.objects.get(id = pk)
	comments = post.comments.filter(post_id = True)
	new_comment = None
	if request.method == 'POST':
		comment_form = CommentForm(data = request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit = False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request, 'post_detail.html', {'post' : post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

@login_required
def post_create(request):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	else:
		if request.method == 'POST':
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.save()
				return redirect('post_detail', pk = post.pk)
		else:
			form = PostForm()
	context = {'form' : form, 'header': "Add New Post"}
	return render(request, 'post_form.html', context)

@login_required
def post_edit(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	post = Post.objects.get(pk = pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance = post)
		if form.is_valid():
			post = form.save()
			return redirect('post_detail', pk = post.pk)

	else:
		form = PostForm(instance = post)
	return render(request, 'post_form.html', {'form' : form})

@login_required
def post_delete(request, pk):
	Post.objects.get(id = pk).delete()
	return redirect('profile.html')

# -------- Comment views -------- #
@login_required
def comment_list(request):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	comments = Comment.objects.all()
	return render(request, 'comment_list.html', {'comments' : comments})

def comment_detail(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	comment = Comment.objects(id = pk)
	return render(request, 'comment_detail.html', {'comment' : comment})

@login_required
def comment_create(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			post = Post.objects.get(pk = pk)
			comment.post = post
			comment.user = request.user
			comment.save()
			return redirect('post_detail', pk = post.pk)

	else:
		form = CommentForm()
	context = {'form' : form, 'header' : "Add New Comment"}
	return render(request, 'comment_form.html', context)

@login_required
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

@login_required
def comment_delete(request, pk):
	Comment.objects.get(id = pk).delete()
	return redirect('comment_list')

def global_view(request, query = ''):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			q = form.cleaned_data['query']
			posts = Post.post_query(q)
			print(posts)

			# Return users with global_view
			filtered_users = User.objects.filter(username__icontains = q)
			print(filtered_users)
			return render(request, 'global_view.html', {'posts': posts})

	if (query):
		posts = Post.post_query(query)
		print(posts)
		# Return users with global_view
		filtered_users = User.objects.filter(username__icontains = query)
		print(filtered_users)
		return render(request, 'global_view.html', {'posts': posts})

	posts = Post.post_relevent()

	return render(request, 'global_view.html', {'posts': posts })

@login_required
def like_post(request, post_id):
	# likes = 0
	# if (post_id):
	# 	post = Post.objects.get(id=int(post_id))
	# 	if post is not None:
	# 		likes = post.likes + 1
	# 		post.likes = likes
	# 		post.save()
	# 	print(likes)
	# return HttpResponse(likes)

	likes = 0

	if (post_id) :

		# print(UserLikesPost.objects.filter(user_id = request.user.id, post_id = post_id).exists())
		# print(request.user.username)
		# print(Post.objects.filter(user = request.user.id, id = post_id).exists())

		post = Post.objects.get(id = post_id)

		if post is not None:
			if not UserLikesPost.objects.filter(user_id = request.user.id, post_id = post_id).exists() and not Post.objects.filter(user = request.user.id, id = post_id).exists():

				print('create entry')

				liked_post = UserLikesPost.objects.create(
					user_id = request.user,
					post_id = post,
					)
				liked_post.save()

				user_likes = UserLikesPost.objects.filter(post_id = post_id).count()

				likes = post.likes + user_likes
				post.likes = post.likes + user_likes
				post.save()
				
		likes = UserLikesPost.objects.filter(post_id=post_id).count()
			
	print(likes)	
	return HttpResponse(likes)

@login_required
def activity_list(request):
	return render(request, 'activity_list.html')