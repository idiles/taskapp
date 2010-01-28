from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('search.views',
    # url(r'^$', login_required(views.index), name='find'),
    url(r'^$', 'index', name='index'),
    url(r'^people$', 'people', name='people'),
)
