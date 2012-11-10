from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$', 'studentq.views.index'),
    url(r'^test$', 'studentq.views.test'),
    url(r'^getstate$', 'studentq.views.getstate'),
    url(r'^updatestate$', 'studentq.views.updatestate'),
    url(r'^updateattention$', 'studentq.views.updateattention'),
)

