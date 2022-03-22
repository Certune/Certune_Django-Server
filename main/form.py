from django.forms import ModelForm
from .models import fileUpload

class FileUploadForm(ModelForm):
    class Meta:
        model = fileUpload
        fields = ['name', 'audioFile']