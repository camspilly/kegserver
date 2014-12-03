# Create your views here.
from django.contrib.auth import authenticate, login2
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from account.models import KegUserForm, UserForm
from account import user_utils

import json

def payment(request):
  pass
  
def index(request):
  # /account/
  # display reset pin
  # display add payment option
  # manage stripe
  # view stripe transactions?
  pass

def login(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)

  if user is not None:
    if user.is_active:
      login(request, user)
      redirect('/account')
  else:
    redirect('/account/login')
    return HttpResponse(json.dumps({"error": "invalid login"}), content_type="application/json")

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
    userf = UserForm(request.POST, prefix='user')
    keguserf = KegUserForm(request.POST, prefix='keguser')
    if userf.is_valid() * keguserf.is_valid():
      user = userf.save(commit=False)
      user.username = user.email
      user.save()
      keguser = keguserf.save(commit=False)
      keguser.user = user
      keguser.save()
      return redirect('/helloworld/')
  else:
    userf = UserForm(prefix='user')
    keguserf = KegUserForm(prefix='keguser')
    return render_to_response('templates/account/register.html', 
                           dict(userform=userf,
                            keguserform=keguserf),
                           context_instance=RequestContext(request))

  return redirect('/account/') # redirect to account, display toast that says succesful register

