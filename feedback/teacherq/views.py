from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from teacherq.models import Question, ActiveQuestion

def index(request):
    return render_to_response('teacherq/index.html', {})

def askquestion(request):
	return render_to_response('teacherq/ask_question.html', {})

def submitquestion(request):
	q = request.GET['question']
	newquestion = Question(question = q)
	newquestion.save()
	return HttpResponse(newquestion.__unicode__() + ' added to database')
	#return render_to_response('teacherq/index.html', {})

def viewquestion(request):
	active_questions = ActiveQuestion.objects.all()
	return render(request, 'teacherq/viewactive.html', {'active_questions': active_questions})
 
