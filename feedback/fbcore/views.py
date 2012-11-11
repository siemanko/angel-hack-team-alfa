from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
import django.contrib.auth

def index(request):
    if not request.user.is_authenticated():
      return HttpResponseRedirect('login')
    else:
      return render_to_response('fbcore/index.html', {
                                                        'is_teacher' : request.user.is_staff,
                                                     })

def login(request):
    if len(request.POST) == 0:
        return render_to_response('fbcore/auth.html', {})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(username=username, password=password)
        if user is not None:
            django.contrib.auth.login(request, user)
            return index(request)
        else:
            return render_to_response('fbcore/auth.html', { 'error' : 'wrongdata'})

def logout(request):
    django.contrib.auth.logout(request)
    return render_to_response('fbcore/auth.html', { 'loggedout' : True })
