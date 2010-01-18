from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('account.views',
    # url(r'^$', login_required(views.index), name='list'),

    # Registration
    url(r'^register$', 'register', name='register'),
    url(r'^registered$', 'registered', name='registered'),
)
