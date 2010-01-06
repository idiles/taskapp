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

    url(r'^$', 'django.views.generic.simple.redirect_to', dict(url='/tasks/'),
        name='home'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', dict(next_page='/'),
        name='logout'),
) + patterns('taasks',      # Include tasks app
    (r'^tasks/', include('tasks.urls', namespace='tasks')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_SLUG,
            'django.views.static.serve',
            dict(document_root=settings.MEDIA_ROOT)),
    )

