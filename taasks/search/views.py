import re
from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.db.models import Max, Sum, Q
from django.utils.translation import ugettext as _

from account.models import UserProfile

from forms import SearchPeopleForm


def index(request):
    return redirect(reverse('search:people'))

def search_people(text):
    profiles = UserProfile.objects.filter(Q(name__icontains=text) | \
        Q(user__username__icontains=text))
    return profiles

def people(request):
    form = SearchPeopleForm()
    profiles = []
    text = ''
    
    if 'q' in request.GET:
        form = SearchPeopleForm(request.GET)
        if form.is_valid():
            text = form.cleaned_data['q']
            profiles = search_people(text)
    
    return direct_to_template(request, 'search/people.html', 
        dict(form=form, text=text, profiles=profiles))
    