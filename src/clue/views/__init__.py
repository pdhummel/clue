import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from clue.models import Player

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def clue(request):
    return render_to_response('board.html')

def login_user(request):
    state = "Please log in below..."
    username = password = ''
    response = render_to_response('login.html',{'state':state, 'username': username})
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
                request.session['username'] = username
                Player.objects.get_or_create(name=username)
                response = render_to_response('board.html',{'state':state, 'username': username}, context_instance=RequestContext(request))
            else:
                state = "Your account is not active, please contact the site admin."
                response =render_to_response('login.html',{'state':state, 'username': username}, context_instance=RequestContext(request))
        else:
            state = "Your username and/or password were incorrect."
            response = render_to_response('login.html',{'state':state, 'username': username}, context_instance=RequestContext(request))

    return response










def test_json(request):
    response_data = {}
    response_data['result'] = 'hello world'
    return HttpResponse(json.dumps(response_data), mimetype="application/json")



def add_player_api(request):
    pass

def start_game_api(request):
    pass


def retrieve_game_state_api(request):
    pass




