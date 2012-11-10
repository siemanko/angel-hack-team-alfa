from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from teacherq.models import Question, AnswerOption, ActiveQuestion

def index(request):
    return render_to_response('teacherq/index.html', {})

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
	active_question = ActiveQuestion.objects.get()
	return render(request, 'teacherq/viewactive.html', {'active_question': active_question})
 
