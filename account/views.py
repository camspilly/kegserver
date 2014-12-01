# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from account.models import KegUserForm, UserForm

#def register(request):
    
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
        return render_to_response('templates/register/register.html', 
                                                   dict(userform=userf,
                                                        keguserform=keguserf),
                                                   context_instance=RequestContext(request))

    return redirect('/helloworld/')
