from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from StringIO import StringIO
import urllib2
from django.core.files.base import ContentFile

def redirect_to_form( *args, **kwargs):
     
    if kwargs.get('request').user.is_authenticated():
        kwargs['request'].session.set('saved_email',kwargs.get('request').user.email) 
        return
     
    if not kwargs.get('details').get('email') and not kwargs['request'].session.get('saved_email') and \
       kwargs.get('user') is None:
        
        #return HttpResponseRedirect(reverse("profile_needemail"))
        #return HttpResponseRedirect("%s?action=ask-email" % kwargs.get('request').session.get('next'))
        return HttpResponseRedirect(reverse('social_registration_needemail'))

def email(request, *args, **kwargs):
    
    if request.session.get('saved_email'):
        email = request.session.get('saved_email')
        details = kwargs.get('details')
        details['email'] = email
        return {'details' : details}
    elif not kwargs.get('user') and not kwargs.get('details').get('email'):
        raise Exception('Invalid data: email must not be empty')
    
    

def update_profile(*args, **kwargs):
    
    avatar_url = None
    
    if kwargs.get('backend').name == 'google-oauth2':
        try:
            avatar_url = kwargs['response']['picture']
        except KeyError:
            pass 
    elif kwargs.get('backend').name == 'twitter':
        
        try:
            avatar_url = "http://api.twitter.com/1/users/profile_image?screen_name=%s&size=bigger" % kwargs['response']['screen_name']
        except KeyError:
            pass 
        
    elif kwargs.get('backend').name == 'facebook':
        
        try:
            avatar_url ="http://graph.facebook.com/%s/picture?type=large" % kwargs['response']['username']
        except KeyError:
            pass 
        
    user = kwargs['user']
    if kwargs['is_new'] or not kwargs['user'].get_profile().avatar:
        
        p = user.get_profile()
        
        input_file = StringIO(urllib2.urlopen(avatar_url).read())
        p.avatar.save(str(p.uuid)+'.jpg', ContentFile(input_file.getvalue()), save=True)
        
    if not user.is_active:
        user.is_active = True
        user.save()
        
    