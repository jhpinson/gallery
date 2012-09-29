from django.contrib.auth.views import login as django_login
from auth.forms import AuthenticationForm, SocialRegistrationEmailForm
from django.shortcuts import redirect, render_to_response
from django.template.response import TemplateResponse

from django.views.generic.edit import FormView
from social_auth.utils import setting

from generic_confirmation.models import DeferredAction
from django.http import  HttpResponseRedirect
from django.views.generic.base import View
from django.template.context import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, authenticate

def login(request, *args, **kwargs):
    
    kwargs['template_name'] = 'registration/login.html'
    return django_login(request, *args, **kwargs)

def register(request, *args, **kwargs):
    
    kwargs['template_name'] = 'registration/register.html'
    return django_login(request, *args, **kwargs)

def popup_login(request, *args, **kwargs):
    
    kwargs['template_name'] = 'registration/modal-login.html'
    kwargs['authentication_form'] = AuthenticationForm
    return django_login(request, *args, **kwargs)


def popup_register(request, *args, **kwargs):
    return TemplateResponse(request, 'registration/modal-register.html')


class RegularRegistrationEmailConfirmation(View):
    def get(self, request, *args, **kwargs):
        
        user = DeferredAction.objects.resume_form_save(kwargs.get('token'))
        if user:
            user = authenticate(email=user.email, force=True)
            auth_login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            
            return HttpResponseRedirect("%s?action=registration-succeed" % reverse('home_view'))
            
        else:
            return HttpResponseRedirect("%s?action=token-expired" % reverse('home_view'))
        
    
class SocialRegistrationEmailConfirmation(View):
    
    def get(self, request, *args, **kwargs):
        
        action = DeferredAction.objects.confirm(kwargs.get('token'))
        if action:
            session_data = action.form_input
            action.delete() 
            
            session = request.session
            for key, value in session_data.iteritems():
                session[key] = value
            
            name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
            
            backend = self.request.session[name]['backend']
            return redirect('socialauth_complete', backend=backend)
        else:
            return HttpResponseRedirect("%s?action=token-expired" % reverse('home_view'))
        

class SocialRegistrationNeedEmail(FormView):
    
    form_class = SocialRegistrationEmailForm
    template_name = "registration/modal_social_registration_email_form.html"
    
    def form_valid(self, form):
        
        form.save(request = self.request)
        return render_to_response('registration/confirmation.html',context_instance=RequestContext(self.request))
    