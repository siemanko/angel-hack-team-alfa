import json
from django.http import HttpResponse, HttpResponseBadRequest, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from studentq.models import Question
from teacherq.models import User

def index(request):
    return render_to_response('studentq/index.html', 
                              {
                                'is_teacher' : User.objects.get(id=1).is_teacher
                              })

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

def getstate(request):
    response = {}
    state = {}
    response['state'] = state
    questions = []
    state['questions'] = questions
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
      q.save()
    return HttpResponse('OK')
      
def updateattention(req):
  user = User.objects.get(id=1)
  if req.GET["change"] == "true":
    user.is_confused = not user.is_confused
    user.save()
  response = { "isConfused" : user.is_confused}
  return HttpResponse(json.dumps(response), mimetype="application/json")
