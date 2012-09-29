from django.conf.urls.defaults import patterns, url
from django.views.generic.base import TemplateView

urlpatterns = patterns('generic_confirmation.views',
    #url(r'^$', 'confirm_by_form', {}, name="generic_confirmation_by_form"),
    #url(r'^(?P<token>\w+)$', 'confirm_by_get', {}, name="generic_confirmation_by_get"),
    (r'^token-expired/$', TemplateView.as_view(template_name="generic_confirmation/modal_token_expired.html"), {}, "token_expired"),
)
