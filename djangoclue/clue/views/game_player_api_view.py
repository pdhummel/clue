from clue.models import GamePlayer
from clue.serializers import GamePlayerSerializer, GamePlayerListSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class GamePlayerList(generics.ListCreateAPIView):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerListSerializer

    def get_queryset(self):
        game_pk = self.kwargs['game_pk']
        return self.queryset.filter(game__pk=game_pk)

    def pre_save(self, obj):
        obj.game_id = self.kwargs['game_pk'] 

        
class GamePlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GamePlayer.objects.all()
    serializer_class = GamePlayerSerializer

