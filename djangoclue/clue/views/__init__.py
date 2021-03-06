import json
import uuid

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from clue.models import Player, Game, GamePlayer


def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def clue(request):
    try:
        if request.COOKIES.has_key('clue_token'):
            token = request.COOKIES['clue_token']
            player = Player.objects.get(token=token)
            return game_list(request, token)
        else:
            state = "Please log in below..."
            response = render_to_response('login.html',{'state':state})
    except:
        state = "Please log in below..."
        response = render_to_response('login.html',{'state':state})   
    return response


def join_game(request):
    data = request.GET
    game_id = int(data['game_id'])
    piece = data['piece']
    game = None
    game_player = None
    try:
        game = Game.objects.get(id=game_id)
    except:
        # TODO:  this is an error
        pass
    
    if request.COOKIES.has_key('clue_token'):
        token = request.COOKIES['clue_token']
        try:
            player = Player.objects.get(token=token)
            game.add_player(player, piece)
        except:
            # TODO:  this is an error
            pass
    else:
        # TODO:  this is an error
        pass
    response = game_board(request, game, game_player)
    return response    
    
    
def enter_game(request):
    response = game_board(request)
    return response

def game_board(request, game=None, game_player=None):
    if game == None:
        data = request.GET
        game_id = int(data['game_id'])
        
        try:
            game = Game.objects.get(id=game_id)
        except:
            # TODO:  this is an error
            pass
    
    response = render_to_response('board.html', {'game': game, 'game_player': game_player})
    return response



def login_user(request):
    page = 'login.html'
    state = "Please log in below..."
    username = ''
    password = ''
    player = None
    
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
            return game_list(request, player.token)
    except:
        state = "Your username and/or password were incorrect."

    response = render_to_response(page,{'state':state, 'username': username})
    if player and player.token:
        response.set_cookie('clue_token', player.token)
        
    return response



def game_list(request, token=None):
    player = None
    try:
        if not token and request.COOKIES.has_key( 'clue_token' ):
            token = request.COOKIES[ 'clue_token' ]
        if token:
            player = Player.objects.get(token=token)
    except Exception, e:
        pass
    
    games = []
    for game in Game.objects.filter():
        game.owner = ""        
        game.players = ""
        game.actions = ["enter"]
        game_player_names = []
        for game_player in GamePlayer.objects.filter(game=game):
            if game_player.is_game_organizer:
                game.owner = game_player.player.name
            if len(game.players) > 0:
                game.players = game.players + ", " + game_player.player.name
            else:
                game.players = game_player.player.name
            game_player_names.append(game_player.player.name)
        
        if player != None:
            # abort | start | join | enter
            if game.game_state == "forming":
                try:
                    game_player = GamePlayer.objects.get(game=game, player=player)
                    if game_player.is_game_organizer == True:
                        if len(game_player_names) >= 3:
                            game.actions.append("start")
                        game.actions.append("abort")
                except:
                    game.actions.append("join")
        games.append(game)            
    
    response = render_to_response('game_list.html', {'player': player, 'games': games})
    # This is here b/c the login screen is not sending it's own response.
    if player and player.token:
        response.set_cookie('clue_token', player.token)    
    return response


