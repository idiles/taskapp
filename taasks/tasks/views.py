from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.db.models import Max

from models import Task


def index(request):
    tasks = Task.objects.all()
    return direct_to_template(request, 'tasks/index.html', dict(
        tasks=tasks))

def new(request):
    return 'Kursim'

def create(request, format=None):
    if format is None:
        format = 'json'
    
    if request.method == 'POST':
        title = request.POST['title']
        position = (Task.objects.aggregate(Max('position'))['position__max'] \
            or 0) + 1
        task = Task(creator=request.user,
            title=title,
            position=position)
        task.save()
    
    return HttpResponse('{format: "%s"}' % format)

def show(request, task_id):
    return 'Rodom %s' % task_id

def edit(request, task_id):
    return 'Atnaujinsim'

def update(request, task_id):
    return 'Atnaujinam'

def delete(request, task_id):
    return 'Trinam', task_id

