from helpers.rest.views import BackboneView
from ..models import Media, Album, Image, DropBox
import json
from django.db import connection
from django.contrib.contenttypes.models import ContentType

class RestMediaView(BackboneView):
    model = Media
    url_root = "rest/medias"
    
    def get(self):
        oid = self.kwargs.get('oid')
        if oid:
            return json.dumps(self.model.objects.get(pk=oid).data)
        else:
            filters = self.get_filters()
            cursor = connection.cursor()
            cursor.execute("SET SESSION group_concat_max_len = 1000000000;")
            
            dropbox_ct = ContentType.objects.get_for_model(DropBox).pk
            
            sql = """
                SELECT group_concat(data) FROM `medias_media` WHERE real_type_id != %s and
            %s='%s' and created_by_id=%s """ % (dropbox_ct, filters.keys()[0], filters.values()[0], self.request.user.pk)
            
            
            cursor.execute(sql)
            res = cursor.fetchall()
            
            return "[%s]" % (res[0][0] if res[0][0] is not None else '')
        
    def put(self):
        oid = self.kwargs.get('oid')
        data = json.loads(self.request.raw_post_data)
        object = self.model.objects.get(pk=oid).cast()
        object.__dict__.update(data)
        object.save()
        return json.dumps(object.toJSON())
        
    def post(self):
        
        data = json.loads(self.request.raw_post_data)
        object = Album.objects.create(**data)
        return json.dumps(object.data)
    
    def get_dropbox(self):
        try:
            return json.dumps(DropBox.objects.get(created_by=self.request.user).data)
        except DropBox.DoesNotExist:
            return json.dumps({})
        
    def get_ancestors(self):
        ancestors = []
        
        ancestor = self.model.objects.get(pk=self.kwargs.get('oid'))
        while (ancestor is not None):
            ancestors.insert(0, ancestor.data)
            ancestor = ancestor.parent_album
        return json.dumps(ancestors)
       
    def put_move(self):
        res = {}
        res['success'] = False
        data = json.loads(self.request.raw_post_data)
        
        album = Album.objects.get(pk=data['album'])
        
        for media in Media.objects.filter(pk__in=data['items']):
            media = media.cast()
            media.parent_album = album
            media.save()
            
        return json.dumps(res)
          
    def put_rotate(self):
        data = json.loads(self.request.raw_post_data)
        image = Image.objects.get(pk=self.kwargs.get('oid'))
        image.rotate(str(data['value']))
        return json.dumps(image.data)
            
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