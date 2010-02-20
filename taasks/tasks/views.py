import re
from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps, loads
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.db.models import Max, Sum
from django.utils.translation import ugettext as _

from forms import TaskForm, ProjectForm
from models import Project, Task, TaskInterval, TaskRegexp

def index(request):
    projects = Project.objects.filter(creator=request.user).all()
    
    form = ProjectForm()
    
    if request.method == 'POST':
        project = Project(creator=request.user, slug='_')
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            request.notifications.add(_(u'Project successfully created'))
            return redirect(reverse('tasks:index'))
        
    return direct_to_template(request, 'tasks/project_index.html', 
        dict(projects=projects, form=form))
    

def tasks(request, project_slug):
    project = Project.get_by_slug(request.user, project_slug)
        
    query_filter = dict(creator=request.user)
    tasks_filter = dict()
        
    if 'tag' in request.GET:
        tag = request.GET['tag']
        query_filter['title__icontains'] = '#%s' % tag
        tasks_filter['class'] = 'tag'
        tasks_filter['value'] = '#%s' % tag
    if 'due' in request.GET:
        due = request.GET['due']
        query_filter['due_date'] = '%s' % due
        tasks_filter['class'] = 'due-date'
        tasks_filter['value'] = '#%s' % due
    
    tasks = project.task_set.filter(**query_filter).exclude(
        removed=True).exclude(archived=True)
        
    children = {}
    for t in tasks:
        children[t.id] = [c.id for c in t.children]
    children_json = dumps(children)
        
    # We can't call a methods with parameters (request.user) in django templates
    # so do the counts here
    for task in tasks:
        task.started = TaskInterval.objects.filter(task=task, doer=request.user,
            duration=None).count() > 0
            
    return direct_to_template(request, 'tasks/index.html', dict(
        project=project, project_slug=project_slug, tasks=tasks,
        children=children_json, tasks_filter=tasks_filter))
        
        
def archive_completed(request, project_slug):
    project = Project.get_by_slug(request.user, project_slug)
    counter = 0
    for task in Task.objects.filter(project=project, creator=request.user, 
        completed=True).exclude(archived=True):
        task.archived = True
        task.save()
        counter += 1
    return HttpResponse(dumps(dict(archived=counter)))
    

def create(request, project_slug):
    if request.method == 'POST':
        title = request.POST['title']
        project = Project.get_by_slug(request.user, project_slug)
        
        tre = TaskRegexp()
        due_date = tre.get_date(title)
        
        position = (Task.objects.filter(
            project=project).aggregate(Max('position'))['position__max'] \
            or 0) + 1
        task = Task(project=project,
            creator=request.user,
            title=title,
            position=position,
            due_date=due_date)
        task.save()
        
        resp = dict(id=task.id, time='0.00', html=task.html)
        resp_json = dumps(resp)
    
        return HttpResponse(resp_json)
        
    return HttpResponse('', status=204)     # No content
    

def update(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        task = form.save()
        tre = TaskRegexp()
        due_date = tre.get_date(task.title)
        task.due_date = due_date
        task.save()
        return HttpResponse(dumps(dict(html=task.html)))
        
        
def indent(request, project_slug, task_id, direction):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    
    if direction == 'left' and task.indent > 0:
        task.increase_indent(-1)
    elif direction == 'right':
        task.increase_indent(1)
        
    return HttpResponse('', status=204)


def sort(request, project_slug):
    if request.method == 'POST':
        project = Project.get_by_slug(request.user, project_slug)
        ids = loads(request.POST['ids'])
        ids = [int(i.replace('task-', '')) for i in ids]
        
        for pos, task_id in enumerate(ids):
            task = get_object_or_404(Task, pk=task_id, project=project)
            task.position = pos
            task.save()
        
    return HttpResponse('', status=204)


def remove(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    task.mark_removed(True)
    for item in TaskInterval.objects.filter(doer=request.user,
        duration=None):
        item.stop()
        item.save()
    return HttpResponse('', status=204)     # No content
    
    
def restore(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    task.mark_removed(False)
    return HttpResponse('', status=204)     # No content
    
    
def mark_done(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id)
    task.mark_completed(True)
    return HttpResponse('', status=204)     # No content
    
    
def mark_undone(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    task.mark_completed(False)
    if task.archived:
        task.mark_archived(False)
        request.notifications.add(_(u'Task has been moved back to list'))
    return HttpResponse('', status=204)     # No content


def start(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    task.start(doer=request.user)
    return HttpResponse('', status=204)     # No content
    
    
def stop(request, project_slug, task_id):
    project = Project.get_by_slug(request.user, project_slug)
    task = get_object_or_404(Task, pk=task_id, project=project)
    task.stop(doer=request.user)
    return HttpResponse('', status=204)     # No content
    
    
def get_time_tracker_data(request):
    today = datetime.now().date()
    duration = TaskInterval.get_hours(request.user, today)
    
    response = dict(today='%.2f' % duration)
    response['tasks'] = []
    
    for item in TaskInterval.objects.filter(doer=request.user,
        duration=None):
        task_time = TaskInterval.get_hours(request.user,
            task=item.task)
        response['tasks'].append(dict(id=item.task.id, time='%.2f' % task_time))
    
    return HttpResponse(dumps(response))
    
    
def trash(request, project_slug):
    project = Project.get_by_slug(request.user, project_slug)
    if request.method == 'POST' and 'empty' in request.POST:
        Task.objects.filter(creator=request.user, 
            removed=True).delete()
        request.notifications.add(_(u'Trash is now empty'))
        return redirect(reverse('tasks:tasks', args=(project_slug, )))
    
    tasks = Task.objects.filter(creator=request.user,
        removed=True)
        
    children = {}
    for t in tasks:
        children[t.id] = [c.id for c in t.children]
    children_json = dumps(children)
        
    return direct_to_template(request, 'tasks/trash.html', dict(
        project=project, project_slug=project_slug, tasks=tasks,
        children=children_json))
        
        
def archive(request, project_slug):
    project = Project.get_by_slug(request.user, project_slug)
    tasks = Task.objects.filter(creator=request.user,
        archived=True).exclude(removed=True)
        
    children = {}
    for t in tasks:
        children[t.id] = [c.id for c in t.children]
    children_json = dumps(children)
        
    return direct_to_template(request, 'tasks/archive.html', dict(
        project=project, project_slug=project_slug, tasks=tasks,
        children=children_json))


def manage(request, project_slug):
    project = Project.get_by_slug(request.user, project_slug)
    
    if request.method == 'POST':
        if 'save' in request.POST:
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                form.user = request.user
                project = form.save()
                request.notifications.add(_(u'Project information updated'))
                return redirect(reverse('tasks:manage', args=(project.slug,)))
        elif 'delete' in request.POST:
            project_title = project.title
            project.task_set.all().delete()
            project.delete()
            request.notifications.add(_(u'Project "%s" has been deleted') \
                % project_title)
            return redirect(reverse('tasks:index'))
        
    form = ProjectForm(instance=project)

    return direct_to_template(request, 'tasks/manage_project.html', dict(
        project_slug=project_slug, project=project, form=form))
