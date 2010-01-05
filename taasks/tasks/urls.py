from django.conf.urls.defaults import *

urlpatterns = patterns('tasks.views',
    url(r'^$', 'index', name='list'),
    (r'^new$', 'new'),
    (r'^create(.(?P<format>json))?$', 'create'),
    (r'^(?P<task_id>\d+)/$', 'show'),
    (r'^(?P<task_id>\d+)/edit$', 'edit'),
    (r'^(?P<task_id>\d+)/update$', 'update'),
    (r'^(?P<task_id>\d+)/delete$', 'delete'),
)
