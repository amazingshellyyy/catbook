from django.urls import path, include
from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views
from main_app.views import profile

urlpatterns = [
    path('<int:pk>/edit', views.profile_edit, name='profile_edit'),
    url(r'^', include('allauth.urls')),
   
]
