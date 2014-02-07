import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from clue.models import Game, Player
from clue.serializers import GameSerializer, GameListSerializer, GameSecretSerializer


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameListSerializer
    
    # create the game
    def post(self, request, *args, **kwargs):
        data = request.DATA
        response_data = {}
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            # data = {"game_name": "first", "player_name": "Paul", "piece": "PP" }
            # TODO:  validate fields
            game_name = None
            if 'game_name' in data:
                game_name = data['game_name']
            player_name = data['player_name']
            piece = data['piece']
            player = Player.objects.get(name=player_name)
            game = Game.objects.create(name=game_name)
            game.add_player(player, piece, True)
            response_status = status.HTTP_201_CREATED
        except Exception, e:
            print e
            response_data['error'] = str(e)
        response = HttpResponse(json.dumps(response_data), status=response_status, 
                            mimetype="application/json")
        return response
    
    

class GameSecretDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSecretSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
    # start the game
    def put(self, request, *args, **kwargs):
        data = request.DATA
        response_data = {}
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            # data = {u'action': u'start_game'}
            # kwargs = {'pk': u'1'}
            game_id = int(kwargs['pk'])
            game = Game.objects.get(id=game_id)
            game.start_game()
            response_status = status.HTTP_200_OK
        except Exception, e:
            print e
            response_data['error'] = str(e)
        return HttpResponse(json.dumps(response_data), status=response_status, 
                            mimetype="application/json")    

    # end the game
    def delete(self, request, *args, **kwargs):
        data = request.DATA
        response_data = {}
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            # kwargs = {'pk': u'1'}
            game_id = int(kwargs['pk'])
            game = Game.objects.get(id=game_id)
            game.end_game()
            response_status = status.HTTP_200_OK
        except Exception, e:
            print e
            response_data['error'] = str(e)
        return HttpResponse(json.dumps(response_data), status=response_status, 
                            mimetype="application/json")




