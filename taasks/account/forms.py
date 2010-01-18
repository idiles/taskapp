# encoding: utf-8

from datetime import datetime, timedelta
import re

from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.forms.forms import BoundField
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=6, max_length=20,
        widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count():
            raise forms.ValidationError(_(u'Not unique!'))
        return username
    
    def save(self):
        user = User(username=self.cleaned_data['username'],
            email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password'])
        user.save()
        profile = user.get_profile()
        profile.full_name = self.cleaned_data['full_name']
        profile.save()
        return user
        