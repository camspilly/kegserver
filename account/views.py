# Create your views here.
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from account.models import KegUserForm, UserForm
from account import user_utils
from account import stripe

import json


def index(request):
  # /account/
  # display reset pin
  # display add payment option
  # manage stripe
  # view stripe transactions?
  pass

def purchase(request)
  user = KegUser.objects.get(user = request.user)
  stripe.charge(request.)

def index(request):
  if request.user.is_authenticated():
    return render_to_response('templates/account/login.html', 
                           {"error": "invalid login"},
                           context_instance=RequestContext(request))

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
      if user.is_active:
        login(request, user)
        redirect('/account')
    else:
      return render_to_response('templates/account/login.html', 
                             {"error": "invalid login"},
                             context_instance=RequestContext(request))
  else:
    if not request.user.is_authenticated():
      return render_to_response('templates/account/login.html', 
                             context_instance=RequestContext(request))
    else:
      return redirect('/account')



def resetpin(request):
  if request.user.is_authenticated():
    user = KegUser.objects.get(user = request.user)
    response_data = {}
    userpin = user_utils.generatepin(5)
    response_data['pin'] = userpin
    user.pin = userpin
    user.save()
    return HttpResponse(json.dumps(response_data), content_type="application/json")
  else:
    return HttpResponse(json.dumps({"error": "user not authenticated"}))


def register(request):
  if request.method == 'POST':
    print "POSTing to register!"
    userf = UserForm(request.POST, prefix='user')
    keguserf = KegUserForm(request.POST, prefix='keguser')
    if userf.is_valid() * keguserf.is_valid():
      print "good register!"
      user = userf.save(commit=False)
      user.username = user.email
      keguser = keguserf.save(commit=False)
      keguser.pin = user_utils.generatepin(5)
      user.save()
      keguser.user = user
      keguser.save()
      return redirect('/account/') # redirect to account, display toast that says succesful register
    print "bad register!"
    userf = UserForm(prefix='user')
    keguserf = KegUserForm(prefix='keguser')
    return render_to_response('templates/account/register.html', 
                           dict(userform=userf,
                            keguserform=keguserf),
                           context_instance=RequestContext(request))
    
  else:
    print "Loading register!"
    userf = UserForm(prefix='user')
    keguserf = KegUserForm(prefix='keguser')
    return render_to_response('templates/account/register.html', 
                           dict(userform=userf,
                            keguserform=keguserf),
                           context_instance=RequestContext(request))

def pinToUser(request):
  user = KegUser.objects.get(pin = request.pin)

  if user is None:
    return HttpResponse(0)
  else:
    return HttpResponse()

