import re

from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.db.models import Max

from forms import TaskForm
from models import Task, TaskInterval, TaskRegexp

def index(request):
    tasks = Task.objects.exclude(removed=True)
    
    # We can't call a methods with parameters (request.user) in django templates
    # so do the counts here
    for task in tasks:
        task.started = TaskInterval.objects.filter(task=task, doer=request.user,
            duration=None).count() > 0
            
    return direct_to_template(request, 'tasks/index.html', dict(
        tasks=tasks))


def create(request, format=None):
    if format is None:
        format = 'json'
    
    if request.method == 'POST':
        title = request.POST['title']
        
        tre = TaskRegexp()
        due_date = tre.get_date(title)['date']
        
        position = (Task.objects.aggregate(Max('position'))['position__max'] \
            or 0) + 1
        task = Task(creator=request.user,
            title=title,
            position=position,
            due_date=due_date)
        task.save()
        
    resp = dict(format=format, id=task.id, html=task.html)
    resp_json = dumps(resp)
    
    return HttpResponse(resp_json)
    

def update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        task = form.save()
        tre = TaskRegexp()
        due_date = tre.get_date(task.title)['date']
        task.due_date = due_date
        task.save()
        return HttpResponse(dumps(dict(html=task.html)))


def remove(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.removed = True
    task.save()
    return HttpResponse('', status=204)     # No content
    
    
def restore(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.removed = False
    task.save()
    return HttpResponse('', status=204)     # No content
    
    
def mark_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    return HttpResponse('', status=204)     # No content
    
    
def mark_undone(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = False
    task.save()
    return HttpResponse('', status=204)     # No content


def start(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.start(doer=request.user)
    return HttpResponse('', status=204)     # No content
    
    
def stop(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.stop(doer=request.user)
    return HttpResponse('', status=204)     # No content
    
    
def trash(request):
    if request.method == 'POST' and 'empty' in request.POST:
        Task.objects.filter(creator=request.user, 
            removed=True).delete()
        return redirect(reverse('tasks:list'))
    
    tasks = Task.objects.filter(creator=request.user,
        removed=True)
        
    return direct_to_template(request, 'tasks/trash.html', dict(
        tasks=tasks))
        