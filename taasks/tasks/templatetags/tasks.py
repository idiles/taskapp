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
        
        
@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value or 0)
    