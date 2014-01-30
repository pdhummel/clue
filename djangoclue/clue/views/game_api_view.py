from clue.models import Game
from clue.serializers import GameSerializer, GameListSerializer, GameSecretSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameListSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameSecretDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSecretSerializer
