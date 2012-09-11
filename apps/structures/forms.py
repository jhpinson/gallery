from django.forms.models import ModelForm
from structures.models import Album
from django.forms.widgets import HiddenInput

class AlbumForm(ModelForm):
    
    class Meta:
        model = Album
        widgets = {
            'parent': HiddenInput,
        }