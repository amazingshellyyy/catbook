from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Post, Comment, UserLikesPost, FollowingUser
from .forms import PostForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from faker import Faker

# *******Fake Data*********
# NOTE: This function is called in on the landing page to create the fake data. If you do not comment it out, you will make a lot of entries
def load_fake():
	default_pass = '1234'
	fake = Faker()
	
	# print(fake.date_time_this_month(before_now=True, after_now=False, tzinfo=None))

	if(User.objects.all().count() <= 5):
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

	print(User.objects.all().count())

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


@login_required
def profile(request, pk=None):
	print('i am profile view')
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	if pk == None:
		user = request.user
	else:
		user = User.objects.get(pk=pk)
	print(user)
	print(f'request user {request.user}')
	posts = Post.objects.filter(user=user)
	followers = FollowingUser.objects.filter(follow_user_id = user)
	comments = Comment.objects.filter()
	follower_count = FollowingUser.objects.filter(follow_user_id = user).count()

	# ========== Changes from Submaster ======
	# return render(request, 'profile.html', {'user':user, 'posts' : posts, 'comments': comments})


	# ****Check if current user is not viewing their profile
	if (request.user.id != pk and request.user != user):
		current_user = False
		# ******Check if current user is following this person
		following = FollowingUser.objects.filter(user_id = request.user.id, follow_user_id = pk).exists()
		return render(request, 'profile.html', {'user': user, 'posts': posts, 'following': following, 'current_user': current_user, 'followers': followers, 'comments': comments, 'follower_count': follower_count})
	else:
		current_user = True
	following = False
	print(current_user)

	return render(request, 'profile.html', {'user':user, 'posts' : posts, 'following': following, 'current_user': current_user, 'followers': followers, 'comments': comments, 'follower_count': follower_count})

# -------- Post views -------- #
def post_detail(request, pk):
	if(is_search_requested(request)):
		return redirect('global_view', request.POST['query'])
	post = Post.objects.get(id = pk)
	comments = Comment.objects.filter(post = post)
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
	print(HttpResponse(likes))
	return HttpResponse(likes)

@login_required
def activity_list(request):
	return render(request, 'activity_list.html')

def about_us(request):
	return render(request, 'about_us.html')
	
@login_required
def follow_user(request, f_user_id):

	print(request.user)

	following = False

	if f_user_id is not None:
		follow_user = User.objects.get(id = f_user_id)

		print(FollowingUser.objects.filter(user_id = request.user.id, follow_user_id = f_user_id).exists())
		print((request.user.id != f_user_id))

		if follow_user is not None:
			if not FollowingUser.objects.filter(user_id = request.user.id, follow_user_id = f_user_id).exists() and  (request.user.id != f_user_id):

				print('create follow entry')

				new_follower = FollowingUser.objects.create(
					user_id = request.user,
					follow_user_id  = follow_user,
					)
				new_follower.save()

				following = True
			elif(request.user.id != f_user_id):
				FollowingUser.objects.filter(user_id = request.user.id, follow_user_id = f_user_id).delete()
		user = User.objects.get(id = f_user_id)
		followers = FollowingUser.objects.filter(follow_user_id = user)
		data_followers = [f.user_id.username for f in followers]
	return JsonResponse({"following": following, "followers": data_followers })

def get_followers(request, pk):
	user = User.objects.get(pk = pk)
	followers = FollowingUser.objects.filter(follow_user_id = user)

	data_followers = [f.user_id.username for f in followers]
	return JsonResponse({"followers": data_followers})

