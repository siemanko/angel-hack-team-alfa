import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from teacherq.models import Question, AnswerOption, UserProfile
import studentq.models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def verify_logged_in(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    else:
        return None
"""
    ver = verify_logged_in(request)
    if ver:
      return ver
"""

def index(request):
  ver = verify_logged_in(request)
  if ver:
      return ver
  questions = []
  for question in studentq.models.Question.objects.order_by('-votescore')[:2]:
    questions.append({ 
                        'text' : question.text,
                        'score' : question.votescore,
                     })

  return render_to_response('teacherq/index.html', 
		{"questions" : questions})

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
	params = {}

	try:
		active_question = ActiveQuestion.objects.get()
		answer_options = AnswerOption.objects.filter(question=active_question)
		params = {
				'active_question': active_question,
				'answer_options': answer_options
				}
	except Exception, e:
		pass

	return render(request, 'teacherq/viewactive.html', params)
 
def submitanswer(request):
	id = request.GET['answer']
	answer = AnswerOption.objects.get(id=id)
	
	existing_answers = QuestionAnswer.objects.filter(user=request.user, question=answer.question)
	
	if (existing_answers.count() != 0):
		return HttpResponse('question already answered')
	
	
	answer.count = answer.count + 1
	answer.save()
	
	useranswer = QuestionAnswer(user=request.user, question=answer.question, answer=answer)
	useranswer.save()
	
	return HttpResponse('question answered')


def showanswers(request):
 	id = request.GET['id']

 	question = Question.objects.get(id=id)
 
	answers = {}

 	for ans in AnswerOption.objects.filter(question__id=id):
 	 	answers[ans.answer] = ans.count

 	return render(request, 'teacherq/show_answers.html', {
 		'question' : question.question,
 		'answers': answers,
 		})

def confusedstudents(request):
	confused_users = UserProfile.objects.filter(is_confused=True).count()
	total_users = UserProfile.objects.all().count()
	confusion_level = confused_users * 100 / total_users

	response = { 'confusionLevel' : confusion_level }
	return HttpResponse(json.dumps(response), mimetype='application/json')


def showconfusion(request):
	return render(request, 'teacherq/showconfusion.html', {} )


def test(request):
		
	for n in range(0, 20):
		newuser = User(username=("student"+n),password="p"+n)
	 	newuser.save()
		create_user_profile(None, newuser, True)

	for n in range(0, 5):
		newuser = User(username="teacher"+n,password="p"+n, is_staff=True)
	 	newuser.save()
		create_user_profile(None, newuser, True)
	
	

	return HttpResponse('test succesfull')
