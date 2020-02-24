from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileEditForm


# Check if User Searches
def is_search_requested(request):
  if request.method == 'POST':
    if 'query' in request.POST.keys():
      return True
    return False
  return False

# Create your views here.
def signup(request):
  # if user search redirect to global view
  if(is_search_requested(request)):
    return redirect('global_view', request.POST['query'])
  # if post
  if request.method == "POST":
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    
  # validate that passwords match
    if password == password2:
      # check if username exists in db
      if User.objects.filter(username=username).exists():
        context = {'error': 'Username is already taken.'}
        return render(request, 'signup.html', context)
      else:
        if User.objects.filter(email=email).exists():
          context = {'error':'That email already exists.'}
          return render(request, 'signup.html', context)
        else: 
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,)
            user.save()
            return redirect('login')
    else:
      context = {'error':'Passwords do not match'}
      return render(request, 'signup.html', context)
  else:
    # if not post send form 
      return render(request, 'signup.html')


def login(request):
  # if user search redirect to global view
  if(is_search_requested(request)):
    return redirect('global_view', request.POST['query'])

  if request.method == 'POST':
    username_form = request.POST['username']
    password_form = request.POST['password']
    # authenticate user
    user = auth.authenticate(username=username_form, password=password_form)
    if user is not None:
      # login
      auth.login(request, user)
      #redirect
      return redirect('profile', pk=user.pk )
      
    else:
      context = {'error':'Invalid Credentials'}
      return render(request, 'login.html', context)
  else:
      return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def profile_edit(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
      form = ProfileEditForm(request.POST, instance=user)
      user = form.save()
      return redirect('profile', pk=user.pk)
    else:
      form = ProfileEditForm(instance=user)
      return render(request,'profile_form.html', {'form':form})  
  