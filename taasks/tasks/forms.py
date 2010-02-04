from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import slugify

from models import Task, Project

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title',)


class ProjectForm(ModelForm):
    title = forms.CharField()
    goal = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Project
        fields = ('title', 'goal')
        exclude = ('creator', 'slug',)
        
    def save(self):
        project = super(ProjectForm, self).save(commit=False)
        title = self.cleaned_data['title']
        project.slug = slugify(title)
        project.save()
        
        return project
        