from django import forms
from .models import Image
from django.utils.translation import ugettext_lazy as _

class ImageForm(forms.Form):
    class Meta:
        model = Image
        fields = ['upload', ]
        labels = {
            'upload':_('choose image')
        }

       