from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from teacherq import views

urlpatterns = patterns('',
        url(r'^$', 'teacherq.views.index', name='teacherq'),
	url(r'^askquestion/$', views.askquestion, name='askquestion'),
	url(r'^askquestion/submitquestion$', views.submitquestion, name='submitquestion'),
	url(r'^viewactive/$', views.viewquestion, name='viewquestion'),
	url(r'^viewactive/submitanswer$', views.submitanswer, name='submitanswer'),
	url(r'^showanswers/(?P<pk>\d+)$', views.showanswers, name='show_answer'),
	url(r'^showconfusion/$', views.showconfusion, name='showconfusion'),
	url(r'^confusedstudents/$', views.confusedstudents, name='confusedstudents'),
	url(r'^test/$', views.test, name='test'),
        url(r'^getquestions$', views.getquestions),
        url(r'^activatequestion/(?P<pk>\d+)$', views.activatequestion),
        url(r'^deactivatequestion$', views.deactivatequestion),
        url(r'^getanswers$', views.getanswers),
)

