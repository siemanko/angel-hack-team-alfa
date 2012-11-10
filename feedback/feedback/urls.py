from django.conf.urls import patterns, include, url
from data_specific_to_me import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'feedback.views.home', name='home'),
    # url(r'^feedback/', include('feedback.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?:index)?$', 'fbcore.views.index'),
    url(r'^studentq/', include('studentq.urls')),
    url(r'^teacherq/', include('teacherq.urls')),
    url(r'^login$', 'fbcore.views.login', name='login'),
    url(r'^logout$', 'fbcore.views.logout'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': PROJECT_DIR + '/static', 'show_indexes': True}
    ),
)
