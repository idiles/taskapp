from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.simplejson import dumps
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from forms import RegistrationForm, ProfileSettingsForm, ProfilePictureForm

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
            request.notifications.add(_(u'Your settings have been updated'))
            return redirect(reverse('account:settings'))
    
    return direct_to_template(request, 'account/settings.html', 
        dict(form=form))
        
        
def picture(request):
    profile = request.user.get_profile()
    form = ProfilePictureForm(profile)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            profile.picture.delete()
            profile.save()
            request.notifications.add(_(u'Your account picture has been removed'))
            return redirect(reverse('account:picture'))
        else:
            form = ProfilePictureForm(profile, request.POST, request.FILES)
            if form.is_valid():
                form.save()
                request.notifications.add(_(u'Your account picture has been updated'))
                return redirect(reverse('account:picture'))
    
    return direct_to_template(request, 'account/picture.html', 
        dict(profile=profile, form=form))
        
        
def connect(request, username):
    user = User.objects.get(username=username)
    # print user.id
    return HttpResponse()