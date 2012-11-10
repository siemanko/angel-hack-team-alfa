from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from teacherq.models import Question

def index(request):
	questions = {}

	for question in Question.objects.all():
		questions[question.id] = question.question

	return render_to_response('teacherq/index.html', questions)

def askquestion(request):
	return render_to_response('teacherq/ask_question.html', {})

def submitquestion(request):
	q = request.GET['question']
	newquestion = Question(question = q)
	newquestion.save()
	return HttpResponse(newquestion.__unicode__() + ' added to database')
	#return render_to_response('teacherq/index.html', {})
