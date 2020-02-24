from django import forms
from .models import Image


class ImageForm(forms.Form):
    class Meta:
        model = Image
        fields = ['upload', ]
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user')
    #     super(ImageForm, self).__init__(*args, **kwargs)
    