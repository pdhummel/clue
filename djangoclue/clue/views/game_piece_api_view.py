import json

from django.http import Http404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from clue.models import GamePiece
from clue.serializers import GamePieceSerializer
from clue.models.constants import CHARACTER_CHOICES


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


@api_view(['GET'])
def piece_list(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps(CHARACTER_CHOICES), mimetype="application/json")

    