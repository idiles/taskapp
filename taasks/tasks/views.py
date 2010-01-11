from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template(request, 'tasks/index.html', dict(
        tasks=[]))

def new(request):
    return 'Kursim'

def create(request, format=None):
    if format is None:
        format = 'json'
    text = 'kitas'
    return HttpResponse('{id: 1, html: "%s"}' % text)

def show(request, task_id):
    return 'Rodom %s' % task_id

def edit(request, task_id):
    return 'Atnaujinsim'

def update(request, task_id):
    return 'Atnaujinam'

def delete(request, task_id):
    return 'Trinam'

