
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView 
from django.urls import reverse_lazy
from .models import Image, ProfileImage
from .forms import ImageForm
from django.http import HttpResponse, HttpResponseRedirect

class ImageCreateView(CreateView):
    # template_name = 'test_img/image_form.html'
    model = Image
    fields = ['upload', ]
    success_url = reverse_lazy('upload')
    def form_valid(self, form):
        form.instance.user = self.request.user
        print('upload success!')
        return super(ImageCreateView, self).form_valid(form)
        # return redirect('profile')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = Image.objects.all()
        context['images'] = images
        return context


def save_image(request, url):
    new_profileImage = ProfileImage
    new_ProfileImage.image_url = url
    new_profileImage.user=request.user
    new_profileImage.save()
    return render(request, 'index.html')
