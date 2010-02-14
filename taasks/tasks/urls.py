from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('tasks.views',
    url(r'^$', login_required(views.index), name='index'),
    
    url(r'^([\w-]+)/tasks$', login_required(views.tasks), name='tasks'),

    # Create task
    url(r'^([\w-]+)/tasks/create$', 'create', name='create'),
    
    # Update task
    url(r'^([\w-]+)/tasks/(\d+)/update$', 'update', name='update'),
    
    # Mark task as done
    url(r'^([\w-]+)/tasks/(\d+)/status/done$', 'mark_done', 
        name='done'),
        
    # Mark task as not done
    url(r'^([\w-]+)/tasks/(\d+)/status/undone$', 'mark_undone', 
        name='undone'),
    
    # Remove task (move to trash)
    url(r'^([\w-]+)/tasks/(\d+)/remove$', 'remove', name='remove'),
    
    # Restore task (move back from trash)
    url(r'^([\w-]+)/tasks/(\d+)/restore$', 'restore', name='restore'),
    
    # Indent task
    url(r'^([\w-]+)/tasks/(\d+)/indent/(\w+)$', 'indent', name='indent'),
    
    # Sort tasks
    url(r'^([\w-]+)/tasks/sort$', 'sort', name='sort'),
    
    # Start time tracker
    url(r'^([\w-]+)/tasks/(\d+)/start$', 'start', name='start'),
    
    # Stop time tracker
    url(r'^([\w-]+)/tasks/(\d+)/stop$', 'stop', name='stop'),
    
    # Get time tracker data
    url(r'^time$', 'get_time_tracker_data', name='time'),
    
    # Trash
    url(r'^([\w-]+)/trash$', 'trash', name='trash'),
    
    # Archive
    url(r'^([\w-]+)/archive$', 'archive', name='archive'),
    
    # Manage project
    url(r'^([\w-]+)/manage$', 'manage', name='manage'),
    
)
