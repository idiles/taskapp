from simplejson import dumps

from django.http import HttpResponse
from django.template import RequestContext
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.db.models import Max

from forms import TaskForm
from models import Task, TaskInterval

def index(request):
    tasks = Task.objects.all()
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
        position = (Task.objects.aggregate(Max('position'))['position__max'] \
            or 0) + 1
        task = Task(creator=request.user,
            title=title,
            position=position)
        task.save()
        
    resp = dict(format=format, id=task.id)
    resp_json = dumps(resp)
    
    return HttpResponse(resp_json)
    

def update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        task = form.save()
        return HttpResponse(dumps(dict(html=task.title)))


def remove(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = task.STATUS_REMOVED
    task.delete()
    return HttpResponse('', status=204)     # No content


def start(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.start(doer=request.user)
    return HttpResponse('', status=204)     # No content
    
    
def stop(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.stop(doer=request.user)
    return HttpResponse('', status=204)     # No content
    