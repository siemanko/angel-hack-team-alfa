from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from teacherq import views

urlpatterns = patterns('',
    url(r'^$', 'teacherq.views.index'),
	url(r'^askquestion/$', views.askquestion, name='askquestion'),
	url(r'^askquestion/submitquestion$', views.submitquestion, name='submitquestion'),
)

