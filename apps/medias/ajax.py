# encoding: utf-8
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from helpers.dajax import clear_form_errors, set_form_errors
from .forms import AlbumForm
from .models import Album,Image,Media

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


@dajaxice_register
def move(request,  medias, create=False, album_name=None, album_pk=None):
    form_id = 'form-move'
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    
    errors = {}
    if create and (album_name is None or len(album_name) == 0):
        errors['name'] = ['Veuillez saisir un nom pour le nouvel album ou retirer la coche sur "Nouvel album"']
    
    if not create and (album_pk is None or album_pk=='' or not Album.objects.filter(pk=album_pk).exists()):
        errors['name'] = ['Veuillez sélectionner un album']
        
        if album_name is not None:
            errors['name'] = ['%s %s' % (errors['name'][0], 'ou cocher "Nouvel album pour créer un nouvel album"')]
        
    if len(errors.keys()) > 0:
        set_form_errors(dajax, form_id, errors)
        
    else:
        if create:
            album = Album.objects.create(name=album_name)
        else:
            
            album = Album.objects.get(pk=album_pk)
        
        old_album = Media.objects.filter(pk=medias[0])[0].parent_album
        Media.objects.filter(pk__in=medias).update(parent_album=album)
        
        album.consolidate_count()
        old_album.consolidate_count()
        
        dajax.redirect('.')
    
    return dajax.json()

@dajaxice_register
def mass_unremove(request, datas):
    dajax = Dajax()
    
    for d in datas:
        image = Image.objects.get(pk=d['pk'])
        image.status = Image.STATUSES.published
        image.save()
        dajax.add_data({'html_id': d['html_id'], 'media_pk' : d['pk']}, 'callback_media_unremove')
    
    dajax.add_data(None, 'setupMassAction')
    
    return dajax.json()

@dajaxice_register
def unremove(request, pk, html_id, **kwargs):
    dajax = Dajax()
    
    image = Image.objects.get(pk=pk)
    image.status = Image.STATUSES.published
    image.save()
    
    dajax.add_data({'html_id': html_id, 'media_pk' : pk}, 'callback_media_unremove')
    #dajax.redirect('.')
    
    return dajax.json()

@dajaxice_register
def mass_remove(request, datas):
    dajax = Dajax()
    
    for d in datas:
        image = Image.objects.get(pk=d['pk'])
        image.status = Image.STATUSES.deleted
        image.save()
        
        dajax.add_data({'html_id': d['html_id'], 'media_pk' : d['pk']}, 'callback_media_remove')
    
    dajax.add_data(None, 'setupMassAction')
    return dajax.json()

@dajaxice_register
def remove(request, pk, html_id, **kwargs):
    dajax = Dajax()
    
    image = Image.objects.get(pk=pk)
    image.status = Image.STATUSES.deleted
    image.save()
    
    dajax.add_data({'html_id': html_id, 'media_pk' : pk}, 'callback_media_remove')
    #dajax.redirect('.')
    
    return dajax.json()

@dajaxice_register
def mass_rotate(request, datas):
    dajax = Dajax()
    
    for d in datas:
        image = Image.objects.get(pk=d['pk'])
        image.rotate(d['value'])
        
        data = getattr(image,"thumbnail_%s" % d['size'])()
        data['html_id'] = d['html_id']
        
        dajax.add_data(data, 'callback_media_rotate')
    
    dajax.add_data(None, 'setupMassAction')
    return dajax.json()

    
@dajaxice_register
def rotate(request, pk, size, value, html_id):
    dajax = Dajax()
    
    image = Image.objects.get(pk=pk)
    image.rotate(value)
    
    data = getattr(image,"thumbnail_%s" % size)()
    data['html_id'] = html_id
    
    dajax.add_data(data, 'callback_media_rotate')
    
    return dajax.json()
