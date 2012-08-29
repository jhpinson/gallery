from django.views.generic.base import TemplateView
from structure.models import Category
from django.views.generic.list import ListView

class CategoryView(ListView):
    
    template_name = 'category.html'
    paginate_by = 25
    _album = None
    
    def get_album(self):
        
        if self._album is None:
        
            pk = self.kwargs.get('pk', None)
            
            if pk is not None:
                self._album = Category.objects.get(pk=pk)
            else:
                self._album = Category.objects.get(parent=None)
        
        return self._album
        
    def get_queryset(self):
        return self.get_album().media_set.select_subclasses()
    
    def get_context_data(self, **kwargs):
        
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['album'] = self.get_album()
        
        context['breadcrumbs'] = list(self.get_album().get_ancestors()) + [self.get_album()]
        
        return context