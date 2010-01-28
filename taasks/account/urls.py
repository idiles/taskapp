from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required, permission_required

import views

urlpatterns = patterns('account.views',
    # Registration
    url(r'^create$', 'create', name='create'),
    url(r'^thankyou$', 'thankyou', name='thankyou'),
    
    # url(r'^confirm$', 'confirm', name='confirm'),
    
    # url(r'^profile$', 'profile', name='profile'),
    
    url(r'^settings$', 'settings', name='settings'),
    url(r'^picture$', 'picture', name='picture'),
    
    url(r'^connections$', 'connections', name='connections'),
    url(r'^connect/(?P<username>\w+)$', 'connect', name='connect'),
    url(r'^cancel_connection/(?P<username>\w+)$', 'cancel_connection', 
        name='cancel-connection'),
    url(r'^confirm_connection/(?P<username>\w+)$', 'confirm_connection', 
        name='confirm-connection'),
)