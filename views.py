from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

print "lalala"
class MainView(TemplateView):
    
    template_name='backbonejs/index.html'
    
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MainView, self).dispatch( request, *args, **kwargs)