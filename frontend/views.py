from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/essay_site/api/v1/?format=json")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", RequestContext(request,{
        'form': form,
        }))

def index(request):
    return render_to_response("index.html",{})

def userprofile(request):
    pass

def course(request):
    pass

def problem(request):
    pass

def organization(request):
    pass

def essay(request):
    pass

def essaygrade(request):
    pass

def user(request):
    pass

def membership(request):
    pass