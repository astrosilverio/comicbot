# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Comic', fields ['publisher']
        db.create_index(u'comicbot_comic', ['publisher'])

        # Adding index on 'Comic', fields ['name']
        db.create_index(u'comicbot_comic', ['name'])

        # Adding index on 'User', fields ['username']
        db.create_index(u'comicbot_user', ['username'])

        # Adding index on 'User', fields ['email']
        db.create_index(u'comicbot_user', ['email'])

        # Adding index on 'Release', fields ['release_date']
        db.create_index(u'comicbot_release', ['release_date'])


    def backwards(self, orm):
        # Removing index on 'Release', fields ['release_date']
        db.delete_index(u'comicbot_release', ['release_date'])

        # Removing index on 'User', fields ['email']
        db.delete_index(u'comicbot_user', ['email'])

        # Removing index on 'User', fields ['username']
        db.delete_index(u'comicbot_user', ['username'])

        # Removing index on 'Comic', fields ['name']
        db.delete_index(u'comicbot_comic', ['name'])

        # Removing index on 'Comic', fields ['publisher']
        db.delete_index(u'comicbot_comic', ['publisher'])


    models = {
        'comicbot.comic': {
            'Meta': {'object_name': 'Comic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'})
        },
        'comicbot.comicsubscription': {
            'Meta': {'object_name': 'ComicSubscription'},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['comicbot.Comic']"}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hardcover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'subscription_type': ('django.db.models.fields.CharField', [], {'default': "'GO'", 'max_length': '2'}),
            'trade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['comicbot.User']"}),
            'variant_pref': ('django.db.models.fields.CharField', [], {'default': "'BT'", 'max_length': '2'})
        },
        'comicbot.release': {
            'Meta': {'object_name': 'Release'},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recent_releases'", 'to': "orm['comicbot.Comic']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'comicbot.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        }
    }

    complete_apps = ['comicbot']