import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

def index(request):
    return render_to_response('studentq/index.html', {})

def test(request):
    return render_to_response('studentq/test.html', {})

def getstate(request):
    response = {}
    state = {}
    response['state'] = state
    questions = []
    state['questions'] = questions
    q1 = {
             'id' : 1,
             'text' : 'Does Windows 8 sucks more than 7?',
             'votescore' : 10
         }
    q2 = {
             'id' : 2,
             'text' : 'Can I haz pizza?',
             'votescore' : 3
         }
    q3 = {
             'id' : 3,
             'text' : 'Does Windows 8 really sucks more than 7?',
             'votescore' : 13
         }

    questions.append(q1)
    questions.append(q2)
    questions.append(q3)
    return HttpResponse(json.dumps(response), mimetype="application/json")
