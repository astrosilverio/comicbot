# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comic'
        db.create_table(u'comicbot_comic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'comicbot', ['Comic'])

        # Adding model 'User'
        db.create_table(u'comicbot_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
        ))
        db.send_create_signal(u'comicbot', ['User'])

        # Adding model 'ComicSubscription'
        db.create_table(u'comicbot_comicsubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['comicbot.User'])),
            ('comic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['comicbot.Comic'])),
            ('issue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trade', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hardcover', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expire_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('subscription_type', self.gf('django.db.models.fields.CharField')(default='GO', max_length=2)),
            ('variant_pref', self.gf('django.db.models.fields.CharField')(default='BT', max_length=2)),
        ))
        db.send_create_signal(u'comicbot', ['ComicSubscription'])

        # Adding model 'Release'
        db.create_table(u'comicbot_release', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recent_releases', to=orm['comicbot.Comic'])),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'comicbot', ['Release'])


    def backwards(self, orm):
        # Deleting model 'Comic'
        db.delete_table(u'comicbot_comic')

        # Deleting model 'User'
        db.delete_table(u'comicbot_user')

        # Deleting model 'ComicSubscription'
        db.delete_table(u'comicbot_comicsubscription')

        # Deleting model 'Release'
        db.delete_table(u'comicbot_release')


    models = {
        u'comicbot.comic': {
            'Meta': {'object_name': 'Comic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'comicbot.comicsubscription': {
            'Meta': {'object_name': 'ComicSubscription'},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['comicbot.Comic']"}),
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hardcover': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'subscription_type': ('django.db.models.fields.CharField', [], {'default': "'GO'", 'max_length': '2'}),
            'trade': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['comicbot.User']"}),
            'variant_pref': ('django.db.models.fields.CharField', [], {'default': "'BT'", 'max_length': '2'})
        },
        u'comicbot.release': {
            'Meta': {'object_name': 'Release'},
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recent_releases'", 'to': u"orm['comicbot.Comic']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'comicbot.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['comicbot']