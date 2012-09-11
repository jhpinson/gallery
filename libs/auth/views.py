from django.contrib.auth.views import login as django_login
from auth.forms import AuthenticationForm

def popup_login(request, *args, **kwargs):
    
    kwargs['template_name'] = 'registration/modal-login.html'
    kwargs['authentication_form'] = AuthenticationForm
    
    return django_login(request, *args, **kwargs)

def login(request, *args, **kwargs):
    
    kwargs['template_name'] = 'registration/login.html'
    kwargs['authentication_form'] = AuthenticationForm
    
    return django_login(request, *args, **kwargs)