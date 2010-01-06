from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.index), name='list'),
    (r'^new$', permission_required('add_task')(views.new)),
    (r'^create(.(?P<format>json))?$',
        permission_required('add_task')(views.create)),
    (r'^(?P<task_id>\d+)/$', login_required(views.show)),
    (r'^(?P<task_id>\d+)/edit$',
        permission_required('change_task')(views.edit)),
    (r'^(?P<task_id>\d+)/update$',
        permission_required('change_task')(views.update)),
    (r'^(?P<task_id>\d+)/delete$',
        permission_required('delete_task')(views.delete)),
)
