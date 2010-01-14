from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

from utils.dispatch import by_method

import views

urlpatterns = patterns('tasks.views',
    url(r'^$', 'index', name='list'),

    # Create task
    url(r'^create$', 'create', name='create'),
    
    # Update task
    url(r'^(?P<task_id>\d+)/update$', 'update', name='update'),
    
    # Mark task as done
    url(r'^(?P<task_id>\d+)/status/done$', 'mark_done', 
        name='done'),
        
    # Mark task as not done
    url(r'^(?P<task_id>\d+)/status/undone$', 'mark_undone', 
        name='undone'),
    
    # Remove task (move to trash)
    url(r'^(?P<task_id>\d+)/remove$', 'remove', name='remove'),
    
    # Restore task (move back from trash)
    url(r'^(?P<task_id>\d+)/restore$', 'restore', name='restore'),
    
    # Start time tracker
    url(r'^(?P<task_id>\d+)/start$', 'start', name='start'),
    
    # Stop time tracker
    url(r'^(?P<task_id>\d+)/stop$', 'stop', name='stop'),
    
    # View trash
    url(r'^trash$', 'trash', name='trash'),

)
