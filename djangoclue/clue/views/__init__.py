import json
import uuid

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from clue.models import Player


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def clue(request):
    try:
        if request.COOKIES.has_key( 'clue_token' ):
            value = request.COOKIES[ 'clue_token' ]
            player = Player.objects.get(token=value)
            # TODO:  goto the game screen instead
            return render_to_response('board.html')
        else:
            state = "Please log in below..."
            response = render_to_response('login.html',{'state':state})
    except:
        state = "Please log in below..."
        response = render_to_response('login.html',{'state':state})   
    return response


def login_user(request):
    page = 'login.html'
    state = "Please log in below..."
    username = ''
    password = ''
    
    try:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            player, created = Player.objects.get_or_create(name=username, password=password)
            
            if created or not player.token:
                # http://stackoverflow.com/questions/1210458/how-can-i-generate-a-unique-id-in-python
                # The library underlying that module was buggy and forked a process that kept FDs open. 
                # This is to avoid using the native implementation which caused a daemon to be started.
                uuid._uuid_generate_time = None
                uuid._uuid_generate_random = None
                player.token = uuid.uuid4()
                player.save()
                
            page = 'board.html'
    except:
        state = "Your username and/or password were incorrect."

    response = render_to_response(page,{'state':state, 'username': username})
    if player.token:
        response.set_cookie('clue_token', player.token)
        
    return response






