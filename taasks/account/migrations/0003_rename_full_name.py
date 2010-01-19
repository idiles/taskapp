
from south.db import db
from django.db import models
from account.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'UserProfile.name'
        db.add_column('account_userprofile', 'name', orm['account.userprofile:name'])
        
        # Deleting field 'UserProfile.full_name'
        db.delete_column('account_userprofile', 'full_name')
        
        # Changing field 'UserProfile.website'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True, blank=True))
        db.alter_column('account_userprofile', 'website', orm['account.userprofile:website'])
        
        # Changing field 'UserProfile.about'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True, blank=True))
        db.alter_column('account_userprofile', 'about', orm['account.userprofile:about'])
        
        # Changing field 'UserProfile.experience'
        # (to signature: django.db.models.fields.TextField(null=True, blank=True))
        db.alter_column('account_userprofile', 'experience', orm['account.userprofile:experience'])
        
        # Changing field 'UserProfile.timezone'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True, blank=True))
        db.alter_column('account_userprofile', 'timezone', orm['account.userprofile:timezone'])
        
        # Changing field 'UserProfile.location'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True, blank=True))
        db.alter_column('account_userprofile', 'location', orm['account.userprofile:location'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'UserProfile.name'
        db.delete_column('account_userprofile', 'name')
        
        # Adding field 'UserProfile.full_name'
        db.add_column('account_userprofile', 'full_name', orm['account.userprofile:full_name'])
        
        # Changing field 'UserProfile.website'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True))
        db.alter_column('account_userprofile', 'website', orm['account.userprofile:website'])
        
        # Changing field 'UserProfile.about'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True))
        db.alter_column('account_userprofile', 'about', orm['account.userprofile:about'])
        
        # Changing field 'UserProfile.experience'
        # (to signature: django.db.models.fields.TextField(null=True))
        db.alter_column('account_userprofile', 'experience', orm['account.userprofile:experience'])
        
        # Changing field 'UserProfile.timezone'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True))
        db.alter_column('account_userprofile', 'timezone', orm['account.userprofile:timezone'])
        
        # Changing field 'UserProfile.location'
        # (to signature: django.db.models.fields.CharField(max_length=100, null=True))
        db.alter_column('account_userprofile', 'location', orm['account.userprofile:location'])
        
    
    
    models = {
        'account.userprofile': {
            'about': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'experience': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'primary_key': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
