from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('account.views',
    # Registration
    url(r'^create$', 'create', name='create'),
    url(r'^confirm$', 'confirm', name='confirm'),
)
