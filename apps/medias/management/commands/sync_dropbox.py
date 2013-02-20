from django.core.management.base import BaseCommand
from dropbox import client, rest, session
from django.conf import settings
from medias.models import  DropBox
from middleware.request import set_current_user
from django.contrib.auth.models import User
from medias.models import create_media
from dateutil.parser import parse
from django.utils.timezone import get_current_timezone
from django.db.utils import IntegrityError
from django.db import transaction

class Command(BaseCommand):
    
    @transaction.commit_manually
    def handle(self, *args, **options):
        
        set_current_user(User.objects.all()[0])
        
        secret = "k2qcxgc5xh1cdyi"
        token="h6swm06cxy962la"

        sess = session.DropboxSession(settings.DROPBOX_APP_ID, settings.DROPBOX_API_SECRET, "app_folder")
        sess.set_token(token, secret)
        
        cli = client.DropboxClient(sess)
        
        dropbox_album, created = DropBox.objects.get_or_create(name="DROPBOX")
        
        delta = cli.delta(cursor=dropbox_album.delta)
        
        cursor = delta['cursor']
        
        
        for entry in delta['entries']:
            
            if entry[1] is None: continue 
            
            if entry[1]['is_dir'] is True:
                continue
            entry_path = entry[0]
            
            print "processing", entry_path
            
            f, metadata = cli.get_file_and_metadata(entry_path)
            
            try:
                create_media(dropbox_album, f,entry[0].split('/')[-1] , parse(metadata['client_mtime']).astimezone(get_current_timezone()).replace(tzinfo=None))
                f.close()
                transaction.commit()
            except IntegrityError:
                pass
            
            try:
                cli.file_delete(entry_path)
            except rest.ErrorResponse:
                pass
            
        
        dropbox_album.delta = cursor
        dropbox_album.save()
        
        transaction.commit()