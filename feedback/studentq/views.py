import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from teacherq.models import UserProfile
from studentq.models import Question
from teacherq.models import UserQuestionAnswer, AnswerOption

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
    return render_to_response('studentq/index.html', 
                              {
                                'is_teacher' : request.user.get_profile().is_teacher
                              })

def start(request):
    return render_to_response('studentq/start.html', {})

def pacman(request):
    return render_to_response('studentq/pacman.html', {})
    
def test(request):
    return render_to_response('studentq/test.html', {})

def changeuser(request):
    if len(User.objects.all()) == 0:  
        user = User(name = 'angel', is_logged_in = True, is_teacher = False,
is_confused = False)
        user.save();
    else:
        user = User.objects.get(id=1)
        user.is_teacher = not user.is_teacher
        user.save()
    return HttpResponse("OK");

def confusion_level(request):
	confused_users = UserProfile.objects.filter(is_confused=True).count()
	total_users = UserProfile.objects.all().count()
	confusion_level = confused_users * 100 / total_users
	return confusion_level 


def getstate(request):
    response = {}
    state = {}
    response['state'] = state
    questions = []
    state['questions'] = questions
    state['confusion'] = confusion_level(request)
    for q in Question.objects.all():
      questions.append({
                         'id' : q.id,
                         'text' : q.text,
                         'votescore' : q.votescore,
                         'is_answered' : q.is_answered,
                        })
    return HttpResponse(json.dumps(response), mimetype="application/json")

def updatestate(request):
  try:
    action = request.POST['action']
    if action == 'vote':
        qid = request.POST['id']
        q = Question.objects.get(id = qid)
        points = request.POST['points']
    elif action == 'add':
        qtext = request.POST['text']
    elif action == 'mark':
        qid = request.POST['id']
        q = Question.objects.get(id = qid)        
    else:
      throw
  except:
    return HttpResponseBadRequest('FUCK');
  else:
    if action == 'vote':
      q.votescore += int(points)
      q.save()
    elif action == 'add':
      q = Question(text=qtext, votescore=1)
      q.save()
    elif action == 'mark':
      q.is_answered = True
      q.votescore = -1000
      q.save()
    return HttpResponse('OK')
      
def updateattention(request):
  user_profile = request.user.get_profile() 
  if request.GET["change"] == "true":
    user_profile.is_confused = not user_profile.is_confused
    user_profile.save()
  response = { "isConfused" : user_profile.is_confused}
  return HttpResponse(json.dumps(response), mimetype="application/json")

def answerquestion(request):
  id = request.GET["id"]
  answer = QuestionAnswer.objects.get(id = id)
  uqanswer = UserQuestionAnswer(user = request.user, answer = answer);
  uqanswer.save();
  return HttpResponse("OK")  
