from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from teacherq.models import Question, AnswerOption, ActiveQuestion

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
	
	ans_a = AnswerOption(question=newquestion, answer=request.GET['ans_a'], count=0)
	ans_b = AnswerOption(question=newquestion, answer=request.GET['ans_b'], count=0)
	ans_c = AnswerOption(question=newquestion, answer=request.GET['ans_c'], count=0)
	ans_d = AnswerOption(question=newquestion, answer=request.GET['ans_d'], count=0)
	ans_a.save()
	ans_b.save()
	ans_c.save()
	ans_d.save()

	
	return HttpResponse(newquestion.__unicode__() + ' added to database')
	#return render_to_response('teacherq/index.html', {})

def viewquestion(request):
	active_question = ActiveQuestion.objects.all()[0]
	return render(request, 'teacherq/viewactive.html', {'active_questions': active_questions})
 
