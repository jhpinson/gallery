from django.forms.models import ModelForm
from medias.models import Album
from django.forms.widgets import HiddenInput
from django import forms

class AlbumForm(ModelForm):
    
    class Meta:
        model = Album
        widgets = {
            'parent_album': HiddenInput,
        }
        fields = ('name', 'description', 'parent_album',)
        
        
class MoveForm(forms.Form):
    
    name = forms.CharField(label='', max_length=512)
    new_album = forms.BooleanField(label='Nouvel album')
    album_id = forms.IntegerField(widget=forms.HiddenInput)