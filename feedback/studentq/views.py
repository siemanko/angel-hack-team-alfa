from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

def index(request):
    return render_to_response('studentq/index.html', {})

def test(request):
    return render_to_response('studentq/test.html', {})
