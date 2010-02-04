from datetime import datetime

from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.db.models import Max, Sum
from django.utils.translation import ugettext as _


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('tasks:index'))
        
    return direct_to_template(request, 'public/index.html', 
        dict())