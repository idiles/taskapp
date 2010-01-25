from django import template
from django.conf import settings
from django.utils import translation
from django.template import resolve_variable

from taasks.tasks.models import Task, TaskInterval

register = template.Library()

@register.tag
def task_duration(parser, token):
    return TaskDurationNode()

class TaskDurationNode(template.Node):
    def render(self, context):
        task = context.get('task')
        user = context.get('user')
        duration = TaskInterval.get_hours(user=user, task=task)
        return '%.2f' % duration
        