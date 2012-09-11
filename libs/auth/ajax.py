# -*- coding: utf-8 -*-
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from helpers.dajax import clear_form_errors, set_form_errors
from auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

@dajaxice_register
def login(request, form_id, email, password, next=None, **kwargs):
    dajax = Dajax()
    clear_form_errors(dajax, form_id)
    
    form = AuthenticationForm(data={'email' : email, 'password' : password})
    
    if form.is_valid():
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            
        dajax.redirect(next)
    else:
        
        set_form_errors(dajax, form_id, form.errors)
        
    return dajax.json()

