import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from clue.models import Player, GamePlayer, Game
from clue.serializers import GamePlayerSerializer, GamePlayerListSerializer


class GamePlayerList(generics.ListCreateAPIView):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerListSerializer

    def get_queryset(self):
        game_pk = self.kwargs['game_pk']
        return self.queryset.filter(game__pk=game_pk)

    def pre_save(self, obj):
        obj.game_id = self.kwargs['game_pk'] 
        
    def post(self, request, *args, **kwargs):
        # from https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/mixins.py
        data = request.DATA
        response_data = {}
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            name = data['name']
            piece = data['piece']
            is_owner = False
            if 'is_owner' in data and \
                data[is_owner] in ['Y', 'y', 'Yes', 'yes', 'True', 'true']:
                is_owner = True
                
            player, created = Player.objects.get_or_create(name=name)
            response_data['name'] = name
            response_data['player_id'] = player.id
            game_id = int(kwargs['game_pk'])
            game = Game.objects.get(id=game_id)
            game.add_player(player, piece, is_owner)
            response_status = status.HTTP_201_CREATED
        except Exception, e:
            response_data['error'] = str(e)
        return HttpResponse(json.dumps(response_data), status=response_status, 
                            mimetype="application/json")


        
class GamePlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerSerializer

