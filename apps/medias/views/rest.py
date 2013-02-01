from helpers.rest.views import BackboneView
from ..models import Media, Album
import json
from django.db import connection

class RestMediaView(BackboneView):
    model = Media
    url_root = "rest/medias"
    
    def get(self):
        """ Retrieves an object, or a list of objects.
        """
        """filters = self.get_filters()
        #@cached_as(self.model.objects.filter(**filters))
        def _get():
            oid = self.kwargs.get('oid')
            if oid:
                out = self.model.objects.get(pk=oid).toJSON()
            else:
                out = [o.toJSON() for o in self.model.objects.filter(**filters)]
            return json.dumps(out)
        return _get()
        """
        filters = self.get_filters()
        cursor = connection.cursor()
        cursor.execute("SET SESSION group_concat_max_len = 1000000000;")
        
        sql = """
            SELECT group_concat(data) FROM `medias_media` WHERE 
        %s='%s'""" % (filters.keys()[0], filters.values()[0])
        
        
        cursor.execute(sql)
        res = cursor.fetchall()
        return "[%s]" % res[0][0]
        
    def post(self):
        
        data = json.loads(self.request.raw_post_data)
        object = Album.objects.create(**data)
        return json.dumps(object.toJSON())
    
    def get_ancestors(self):
        ancestors = []
        
        ancestor = self.model.objects.get(pk=self.kwargs.get('oid'))
        while (ancestor is not None):
            ancestors.insert(0, ancestor.toJSON())
            ancestor = ancestor.parent_album
        return json.dumps(ancestors)
          
    def put_rotate(self):
        data = json.loads(self.request.raw_post_data)
        image = self.model.objects.get(pk=self.kwargs.get('oid')).cast()
        image.rotate(str(data['value']))
        return json.dumps(image.toJSON())
            
    def get_search(self):
        search = self.request.GET.get('q', None)
        if search is not None:
            qs = Album.objects.filter(name__icontains=search)
        
            return json.dumps([o.data for o in qs])
        else:
            return json.dumps([])
    
    def get_filters(self):
        filter = {}
        
        if self.request.GET.get('is_an_album', None) is not None:
            filter['is_an_album'] = self.request.GET.get('is_an_album', None)
             
        if self.request.GET.get('parent_album_id', None) is not None:
            filter['parent_album_id'] = self.request.GET.get('parent_album_id', None)
            
                
        return filter