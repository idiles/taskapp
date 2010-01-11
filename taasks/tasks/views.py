#from django.core import serializers
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template

from forms import TaskForm
from models import Task

def index(request):
    return direct_to_template(request, 'tasks/index.html', dict(
        tasks=[]))

#def new(request):
#    return 'Kursim'

def create(request):
    task = Task(creator=request.user, position=1)
    form = TaskForm(request.POST, instance=task)
    form.save()
    return HttpResponse(dumps(dict(text=task.title)))

#def show(request, task_id):
#    return 'Rodom %s' % task_id

#def edit(request, task_id):
#    return 'Atnaujinsim'

def update(request, task_id):
    return 'Atnaujinam'

def delete(request, task_id):
    return 'Trinam'

