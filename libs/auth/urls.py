
from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from auth.views import SocialRegistrationNeedEmail, RegularRegistrationEmailConfirmation, SocialRegistrationEmailConfirmation

urlpatterns = patterns('',
    #url(r'^login/$', 'auth.views.login', name='login'),
    url(r'^login/$', 'auth.views.login', name='login'),
    url(r'^popup-login/$', 'auth.views.popup_login', name='popup_login'),
    
    url(r'^register/$', 'auth.views.register', name='register'),
    url(r'^popup-register/$', 'auth.views.popup_register', name='popup_register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    
    url('auth/need-email/', SocialRegistrationNeedEmail.as_view(), name="social_registration_needemail"),
    
    url('auth/social-registration-confirm/(?P<token>.*)/', SocialRegistrationEmailConfirmation.as_view(), name="social_registration_confirm"),
    url('auth/regular-registration-confirm/(?P<token>.*)/', RegularRegistrationEmailConfirmation.as_view(), name="regular_registration_confirm"),
    
    url('auth/confirmation-sent/', TemplateView.as_view(template_name = "registration/modal_confirmation.html"), name="auth_confirmation_sent"),
    
    url('auth/registration-succeed/', TemplateView.as_view(template_name = "registration/modal_registration_succeed.html"), name="registration_succeed"),
    
    
)
