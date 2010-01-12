from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

from utils.dispatch import by_method

import views

urlpatterns = patterns('',
    url(r'^$',
        by_method(
            # List all tasks
            GET=login_required(views.index),
            # Create a new task
            POST=permission_required('add_task')(views.create)),
        name='list'),

    # View the task creation form
    #url(r'^new$',
    #    by_method(GET=permission_required('add_task')(views.new))),

    # Create a new task
    url(r'^create$',
        by_method(POST=permission_required('add_task')(views.create)),
        name='create'),

    url(r'^(?P<task_id>\d+)/$',
        by_method(
            # Show a task
            #GET=login_required(views.show),
            # Modify a task
            PUT=permission_required('change_task')(views.update),
            # Delete a task
            DELETE=permission_required('delete_task')(views.delete))
        ),

    # Show a task modification form
    #url(r'^(?P<task_id>\d+)/edit$',
    #    permission_required('change_task')(views.edit)),

    # Update a task
    url(r'^(?P<task_id>\d+)/update$',
        by_method(POST=permission_required('change_task')(views.update)),
        name='update'),

    # Delete a task
    url(r'^(?P<task_id>\d+)/delete$',
        by_method(POST=permission_required('delete_task')(views.delete)),
        name='delete'),

    # Start a task
    url(r'^(?P<task_id>\d+)/start$',
        by_method(POST=login_required(views.start)),
        name='start'),

    # Stop a task
    url(r'^(?P<task_id>\d+)/stop$',
        by_method(POST=login_required(views.stop)),
        name='stop'),
)
