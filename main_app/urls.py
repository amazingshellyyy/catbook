from django.urls import path, re_path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('posts/new', views.post_create, name = 'post_create'),
	path('posts/<int:pk>', views.post_detail, name = 'post_detail'),
	path('posts/<int:pk>/edit', views.post_edit, name = 'post_edit'),
	path('posts/<int:pk>/delete', views.post_delete, name = 'post_delete'),
	path('comments/', views.comment_list, name = 'comment_list'),
	path('comments/new', views.comment_create, name = 'comment_create'),
	path('comments/<int:pk>', views.comment_detail, name = 'comment_detail'),
	path('comments/<int:pk>/edit', views.comment_edit, name = 'comment_edit'),
	path('comments/<int:pk>/delete', views.comment_delete, name = 'comment_delete'),
	re_path(r'^search/$', views.global_view, name="global_view"),
	path('like_post/<int:post_id>/', views.like_post, name="like_post"),
]