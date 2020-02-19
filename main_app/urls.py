from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index),
	path('search/', views.global_view, name="global_view"),
	path('like_post/<int:post_id>/', views.like_post, name="like_post")
]