# encoding: utf-8

from datetime import datetime, timedelta
import re

from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.forms.forms import BoundField
from django.contrib.auth.models import User

from models import UserProfile


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=50,
        label=_(u'Full name'),
        help_text=_(u'Enter your full name'))
    username = forms.CharField(max_length=20,
        label=_(u'Username'),
        help_text=_(u'http://taasks.com/USERNAME'))
    password = forms.CharField(min_length=6, max_length=20,
        widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise forms.ValidationError(_(u'Username is already taken'))
        return username
    
    def save(self):
        user = User(username=self.cleaned_data['username'],
            email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        profile = user.get_profile()
        profile.name = self.cleaned_data['name']
        profile.save()
        return user
        
        
class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'location', 'website', 'about', 'experience']
    
    website = forms.URLField(label=_(u'Website'),
        required=False)
        
    about = forms.CharField(max_length=50,
        label=_(u'About'),
        widget=forms.Textarea(attrs=dict(rows=4)),
        required=False)
        
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if User.objects.filter(username=username).count():
    #         raise forms.ValidationError(_(u'Username is already taken'))
    #     return username
        