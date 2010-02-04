from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Enable the admin:
    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', 'base.views.index', name='home'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', dict(next_page='/'),
        name='logout'),
        
    # Include tasks app
    (r'^projects/', include('tasks.urls', namespace='tasks')),
    
    # Include accounts app
    (r'^account/', include('account.urls', namespace='account')),
    
    # Include people app
    (r'^search/', include('search.urls', namespace='search')),
    
    url(r'^(?P<username>\w+)$', 'account.views.profile', name='account:profile'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # Custom JS and CSS file handler
        (r'^%s/(?P<path>(js|css)/.*)$' % settings.MEDIA_SLUG,
            'base.views.serve_static', dict(document_root=settings.MEDIA_ROOT)),

        # Static file handler
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_SLUG,
            'django.views.static.serve',
            dict(document_root=settings.MEDIA_ROOT)),

    )
    