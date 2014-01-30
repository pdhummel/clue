from clue.models import GamePiece
from clue.serializers import GamePieceSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class GamePieceList(generics.ListCreateAPIView):
    queryset = GamePiece.objects.all()
    serializer_class = GamePieceSerializer

    def get_queryset(self):
        game_pk = self.kwargs['game_pk']
        return self.queryset.filter(game__pk=game_pk)

    def pre_save(self, obj):
        obj.game_id = self.kwargs['game_pk'] 

        
class GamePieceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GamePiece.objects.all()
    serializer_class = GamePieceSerializer

