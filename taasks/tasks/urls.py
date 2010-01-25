from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('tasks.views',
    url(r'^$', login_required(views.index), name='list'),

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
    
    # Get time tracker data
    url(r'^time$', 'get_time_tracker_data', name='time'),
    
    # Trash
    url(r'^trash$', 'trash', name='trash'),
    
    # Archive
    url(r'^archive$', 'archive', name='archive'),

)
