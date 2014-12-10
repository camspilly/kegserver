# Create your views here.
from django.contrib.auth import authenticate, logout as authlogout, login as authlogin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from account.models import KegUserForm, UserForm
from account import user_utils
from account import stripe_utils
from django.template import Context
from account.models import KegUser, User
import json
from django.core.context_processors import csrf
from django.views.decorators.cache import never_cache
import time
from django.views.decorators.csrf import csrf_exempt
import stripe

@csrf_exempt
def purchase(request):
  if request.method == 'POST':
    if not user_utils.api_auth(request.POST['api_key']):
      return HttpResponse(json.dumps({"error": "api key failure"}))
    user = User.objects.get(username=request.POST['username'])
    keguser = KegUser.objects.get(user=user)

    if not stripe_utils.charge_customer(keguser.stripe_id, request.POST['price']):
      keguser.blocked = True
      return HttpResponse(json.dumps({"error": "credit card declined"}))
    else:
      return HttpResponse(json.dumps({"status": "You were charged: " + str(request.price / 100.0)}))


def add_payment(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      keguser = KegUser.objects.get(user = request.user)
      keguser.stripe_id = stripe_utils.create_customer(request.POST['id'])
      keguser.save()
      return HttpResponse(json.dumps({"status": "successful purchase"}))
    else:
      return render(request, 'templates/account/add_payment.html')


def remove_payment(request):
  if request.user.is_authenticated():
    if request.method == 'POST':
      keguser = KegUser.objects.get(user = request.user)
      keguser.stripe_id = ""
      keguser.save()
      return redirect('/account/')


def index(request):
  if request.user.is_authenticated():
    
    keguser = KegUser.objects.get(user=request.user)
    return render(request, 'templates/account/index.html', Context({"user": request.user, "keguser" : keguser}))
  else:
    return redirect('/account/login')

def login(request):
  if request.method == 'POST':
    print request.POST
    name = request.POST[u'username']
    word = request.POST[u'password']
    user = authenticate(username=name, password=word)

    if user is not None:
      if user.is_active:
        authlogin(request, user)
        return redirect('/account/')
    else:
      return render_to_response('templates/account/login.html', 
                             Context({"error": "invalid login"}),
                             context_instance=RequestContext(request))

  else:
    if not request.user.is_authenticated():
      print "not authenticated?"
      return render_to_response('templates/account/login.html', 
                             context_instance=RequestContext(request))

    else:
      return redirect('/account')

def auth_logout(request):
  authlogout(request)
  return redirect('/account')

def resetpin(request):
  if request.user.is_authenticated():
    user = KegUser.objects.get(user = request.user)
    response_data = {}
    userpin = user_utils.generatepin(5)
    try:
      while  KegUser.objects.get(pin=userpin):
        userpin = user_utils.generatepin(5)
    except:
      pass
    response_data['pin'] = userpin
    user.pin = userpin
    user.save()
    return redirect('/account')
  else:
    return redirect('/login')


def register(request):
  if request.method == 'POST':
    userf = UserForm(request.POST, prefix='user')
    keguserf = KegUserForm(request.POST, prefix='keguser')
    if userf.is_valid() * keguserf.is_valid():
      user = userf.save(commit=False)
      user.set_password(request.POST[u'user-password'])
      user.username = user.email
      keguser = keguserf.save(commit=False)
      keguser.pin = user_utils.generatepin(5)
      keguser.blocked = False
      user.save()
      keguser.user = user
      keguser.save()
      return redirect('/account/') # redirect to account, display toast that says succesful register
    userf = UserForm(prefix='user')
    keguserf = KegUserForm(prefix='keguser')
    return render_to_response('templates/account/register.html', 
                           dict(userform=userf,
                            keguserform=keguserf),
                           context_instance=RequestContext(request))
    
  else:
    userf = UserForm(prefix='user')
    keguserf = KegUserForm(prefix='keguser')
    return render_to_response('templates/account/register.html', 
                           dict(userform=userf,
                            keguserform=keguserf),
                           context_instance=RequestContext(request))
@csrf_exempt
def pinToUser(request):

  if request.method == 'POST':
    if not user_utils.api_auth(request.POST['api_key']):
      return HttpResponse(json.dumps({"error": "api key failure"}))
    user = KegUser.objects.get(pin = request.POST['userid'])

    if user is None:
      return HttpResponse(json.dumps({"error": "incorrect pin"}), content_type="application/json")
    else:
      return HttpResponse(json.dumps({"userid": user.user.username, "phone" : user.phone_number}), content_type="application/json")

