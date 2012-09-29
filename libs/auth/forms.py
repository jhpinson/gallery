from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from generic_confirmation.forms import DeferredFormMixIn
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from generic_confirmation.models import DeferredAction
from helpers.mails import send
from django.core.urlresolvers import reverse
from emailusernames.utils import user_exists
from django.contrib.auth.hashers import make_password


class SocialRegistrationEmailForm(DeferredFormMixIn, forms.Form):
    instance = None
    
    email = forms.EmailField(label = _('Email'), max_length=75)
    
    def save(self, user=None, request = None, **kwargs):
        
        
        if not self.is_valid():
            raise Exception("only call save() on a form after calling is_valid().")
        
        if request is None:
            raise Exception('request must be provided')
        
        
        form_class_name = u"%s.%s" % (self.__class__.__module__, 
                                      self.__class__.__name__)

        data = {'form_class':form_class_name, 'form_input':dict(request.session._get_session() , saved_email=self.cleaned_data['email']), 
                'token':self._gen_token(),}
        
        valid_until = kwargs.pop('valid_until', None)
        if valid_until is None:
            self._get_expiration_date()
        data.update({'valid_until': valid_until})
        
        defer = DeferredAction.objects.create(**data)

        if self.instance is not None:
            # this extra step makes sure that ModelForms for editing and for
            # creating objects both work.
            defer.instance_object = self.instance
            defer.save()

        
        send('registration_verifiy_email', self.cleaned_data['email'], {'link' : reverse('social_registration_confirm', kwargs={'token' : defer.token})})
            
        return defer.token
        
        
    class Meta:
        model = None

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = forms.CharField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    
    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields are case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
    
    
class RegistrationForm(DeferredFormMixIn, ModelForm):
    
    email = forms.CharField(label=_("Email"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if user_exists(email):
            raise forms.ValidationError(_("A user with that email already exists."))
        return email
    
    class Meta:
        model = User
        fields = ("email", "password")
    
    def save(self, user=None, request = None, **kwargs):
        
        
        if not self.is_valid():
            raise Exception("only call save() on a form after calling is_valid().")
        
        if request is None:
            raise Exception('request must be provided')
        
        
        form_class_name = u"%s.%s" % (self.__class__.__module__, 
                                      self.__class__.__name__)
        
        self.data['password'] = make_password(self.data['password'])
        
        data = {'form_class':form_class_name, 'form_input':self.data, 
                'token':self._gen_token(),}
        #
        valid_until = kwargs.pop('valid_until', None)
        if valid_until is None:
            self._get_expiration_date()
        data.update({'valid_until': valid_until})
        
        defer = DeferredAction.objects.create(**data)

        if self.instance is not None:
            # this extra step makes sure that ModelForms for editing and for
            # creating objects both work.
            defer.instance_object = self.instance
            defer.save()

        
        send('registration_verifiy_email', self.cleaned_data['email'], {'link' : reverse('regular_registration_confirm', kwargs={'token' : defer.token})})
            
        return defer.token
    
    