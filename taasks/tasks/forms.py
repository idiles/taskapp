from django.forms import ModelForm

from models import Task, Project

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title',)


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'goal')