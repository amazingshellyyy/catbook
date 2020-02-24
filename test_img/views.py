
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView 
from django.urls import reverse_lazy
from .models import Image
from .forms import ImageForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
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
        user = self.request.user
        images = Image.objects.filter(user = user)
        context['images'] = images
        return context

@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        image = ImageForm(request.POST)
        image.image_url = request.image_url
        image.user = request.user
        image.save()
        return HttpResponseRedirect('http://http://127.0.0.1:8000/')
    else:
        return redirect('profile', pk=request.user.pk)

