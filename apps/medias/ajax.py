# encoding: utf-8
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from helpers.dajax import clear_form_errors, set_form_errors
from .forms import AlbumForm
from .models import Album

@dajaxice_register
def save_album(request, form_id, pk=None, **kwargs):
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    instance = None
    if pk is not None:
        instance = Album.objects.get(pk=pk)
    
    form = AlbumForm(data=kwargs, instance=instance)
    
    if form.is_valid():
        
        try:
            obj = form.save()
            if instance is None:
                dajax.redirect(obj.get_absolute_uri())
            else:
                dajax.redirect('.')
            
        except Exception,e:
            print e
        
        #dajax.add_data(_('Article has been saved'), 'message_success')
    else:
        
        set_form_errors(dajax, form_id, form.errors)
        
    return dajax.json()

