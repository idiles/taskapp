from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User

from forms import RegistrationForm, ProfileSettingsForm

def create(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:thankyou'))
    
    return direct_to_template(request, 'account/create.html', 
        dict(form=form))
    
    
def thankyou(request):
    return direct_to_template(request, 'account/thankyou.html', 
        dict())


# Do we need email confirmation in the first release?
# def confirm(request):
#     return direct_to_template(request, 'account/confirm.html', 
#         dict())


def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.get_profile()
    return direct_to_template(request, 'account/profile.html', 
        dict(profile=profile))


def settings(request):
    profile = request.user.get_profile()
    form = ProfileSettingsForm(profile=profile)
    
    if request.method == 'POST':
        form = ProfileSettingsForm(profile, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('account:settings'))
    
    return direct_to_template(request, 'account/settings.html', 
        dict(form=form))
        