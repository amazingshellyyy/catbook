from django.urls import path, include
from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='social_app/index.html')),
    path('accounts/', include('allauth.urls')),
    path('<int:pk>/edit', views.profile_edit, name='profile_edit'),
    
]
