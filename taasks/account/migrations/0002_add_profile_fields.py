
from south.db import db
from django.db import models
from account.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'UserProfile.location'
        db.add_column('account_userprofile', 'location', orm['account.userprofile:location'])
        
        # Adding field 'UserProfile.about'
        db.add_column('account_userprofile', 'about', orm['account.userprofile:about'])
        
        # Adding field 'UserProfile.experience'
        db.add_column('account_userprofile', 'experience', orm['account.userprofile:experience'])
        
        # Adding field 'UserProfile.website'
        db.add_column('account_userprofile', 'website', orm['account.userprofile:website'])
        
        # Changing field 'UserProfile.full_name'
        # (to signature: django.db.models.fields.CharField(max_length=100))
        db.alter_column('account_userprofile', 'full_name', orm['account.userprofile:full_name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'UserProfile.location'
        db.delete_column('account_userprofile', 'location')
        
        # Deleting field 'UserProfile.about'
        db.delete_column('account_userprofile', 'about')
        
        # Deleting field 'UserProfile.experience'
        db.delete_column('account_userprofile', 'experience')
        
        # Deleting field 'UserProfile.website'
        db.delete_column('account_userprofile', 'website')
        
        # Changing field 'UserProfile.full_name'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True))
        db.alter_column('account_userprofile', 'full_name', orm['account.userprofile:full_name'])
        
    
    
    models = {
        'account.userprofile': {
            'about': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'experience': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['account']
