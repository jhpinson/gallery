# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Media'
        db.create_table('medias_media', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='create_by_media_set', to=orm['auth.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='update_by_media_set', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=2048)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('file', self.gf('filehashfield.fields.FileHashField')(max_length=1024, null=True)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('parent_album', self.gf('django.db.models.fields.related.ForeignKey')(related_name='medias', null=True, to=orm['medias.Album'])),
            ('is_an_album', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('medias', ['Media'])

        # Adding model 'Thumbnail'
        db.create_table('medias_thumbnail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(related_name='thumbnails', to=orm['medias.Media'])),
            ('size', self.gf('django.db.models.fields.CharField')(default='small', max_length=10)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('width', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('medias', ['Thumbnail'])

        # Adding unique constraint on 'Thumbnail', fields ['media', 'size']
        db.create_unique('medias_thumbnail', ['media_id', 'size'])

        # Adding model 'Image'
        db.create_table('medias_image', (
            ('media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['medias.Media'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('medias', ['Image'])

        # Adding model 'Video'
        db.create_table('medias_video', (
            ('media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['medias.Media'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('medias', ['Video'])

        # Adding model 'Album'
        db.create_table('medias_album', (
            ('media_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['medias.Media'], unique=True, primary_key=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('medias', ['Album'])


    def backwards(self, orm):
        # Removing unique constraint on 'Thumbnail', fields ['media', 'size']
        db.delete_unique('medias_thumbnail', ['media_id', 'size'])

        # Deleting model 'Media'
        db.delete_table('medias_media')

        # Deleting model 'Thumbnail'
        db.delete_table('medias_thumbnail')

        # Deleting model 'Image'
        db.delete_table('medias_image')

        # Deleting model 'Video'
        db.delete_table('medias_video')

        # Deleting model 'Album'
        db.delete_table('medias_album')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'medias.album': {
            'Meta': {'ordering': "['-is_an_album', 'date']", 'object_name': 'Album', '_ormbases': ['medias.Media']},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medias.Media']", 'unique': 'True', 'primary_key': 'True'})
        },
        'medias.image': {
            'Meta': {'ordering': "['-is_an_album', 'date']", 'object_name': 'Image', '_ormbases': ['medias.Media']},
            'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medias.Media']", 'unique': 'True', 'primary_key': 'True'})
        },
        'medias.media': {
            'Meta': {'ordering': "['-is_an_album', 'date']", 'object_name': 'Media'},
            'created_at': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'create_by_media_set'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2048'}),
            'file': ('filehashfield.fields.FileHashField', [], {'max_length': '1024', 'null': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_an_album': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified_at': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'update_by_media_set'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'parent_album': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'medias'", 'null': 'True', 'to': "orm['medias.Album']"}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'})
        },
        'medias.thumbnail': {
            'Meta': {'unique_together': "(('media', 'size'),)", 'object_name': 'Thumbnail'},
            'height': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'thumbnails'", 'to': "orm['medias.Media']"}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'small'", 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'medias.video': {
            'Meta': {'ordering': "['-is_an_album', 'date']", 'object_name': 'Video', '_ormbases': ['medias.Media']},
            'media_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['medias.Media']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['medias']