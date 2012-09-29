# -*- coding: utf-8 -*-
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from helpers.dajax import clear_form_errors, set_form_errors
from auth.forms import AuthenticationForm, RegistrationForm, SocialRegistrationEmailForm
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse

@dajaxice_register
def login(request, form_id, email, password, **kwargs):
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    
    form = AuthenticationForm(data={'email' : email, 'password' : password})
    
    if form.is_valid():
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            
        dajax.redirect(kwargs.get('next'))
    else:
        
        set_form_errors(dajax, form_id, form.errors)
        
    return dajax.json()



@dajaxice_register
def register(request, form_id, email, password,  **kwargs):
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    
    form = RegistrationForm(data={'email' : email, 'password' : password})
    if form.is_valid():
        form.save(request = request)
        dajax.script("$('#modal').load('%s')" % reverse('auth_confirmation_sent')) 
    else:
        set_form_errors(dajax, form_id, form.errors)
        
    return dajax.json()


@dajaxice_register
def social_registration_email(request, form_id, email,  **kwargs):
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    form = SocialRegistrationEmailForm(data={'email' : email})
    if form.is_valid():
        
        form.save(request = request)
        
        dajax.script("$('#modal').load('%s')" % reverse('auth_confirmation_sent')) 
    else:
        
        set_form_errors(dajax, form_id, form.errors)
        
    return dajax.json()
