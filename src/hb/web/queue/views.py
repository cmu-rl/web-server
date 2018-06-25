from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from hb.user_server import get_status, add_to_queue 
from .forms import QueueForm

####### helper function ####### 
# assume form.is_valid is false
def getErrMsg(form):
    # update msg here, assume only one error
    error = form.errors.as_data()
    for k,v in error.items():
        msg = str(v[0])[2:-2] # hardcoded formatting
    return msg

def getUserInputFromSignin(request):
    u = request.POST.get('username', None)
    e = request.POST.get('email', None)
    p = request.POST.get('password', None)
    return (u,e,p)
    
####### views ####### 
def form(request):
    isValidInput = True
    msg = "" # for email format and incorrect password
    if request.method == 'POST':
        form = QueueForm(request.POST)
        if form.is_valid():
            # get user input
            (u,e,p) = getUserInputFromSignin(request)
            feedback = add_to_queue(u,e,p) 
            if feedback["error"]: 
                isValidInput = False
                msg = feedback['message']
            else: # success and redirect to status page 
                return HttpResponseRedirect(reverse('queue:status', args=(u,)))
        else: 
            isValidInput = False
            msg = getErrMsg(form)
    else:
        form = QueueForm() 
    return render(request, 'queue/form.html', 
                      {'validInput': isValidInput, 'msg':msg, 'form':form})

# garuntee to have a valide status?
# add some fields in user server, such as ['sent request'] == true
def status(request, username): 
    try:
        status = get_status(username)
    except TimeOut:
        return HttpResponse("server timeout")
    print(status)
    # this should be fixed later by user server update add_to_queue
    # this error should prevent user from directly entering the url
    if status["error"]: return HttpResponse("sorry you haven't sign up yet")
    if status["banned"]: # double check: is this a boolean?
        return render(request, 'queue/banned.html')
    else:
        return render(request, 'queue/status.html',
            {'username':username, 
             'queue_position':status["queue_position"],
             'off_queue':status["off_queue"]})

def index(request):
    return render(request, 'queue/index.html')
