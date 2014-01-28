from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from clue.models import Player
from clue.serializers import PlayerSerializer


# This is no longer used and has been replaced by player_api_view.
@api_view(['GET', 'POST'])
def player_list(request, format=None):
    """
    List all players or create a new player.
    """
    if request.method == 'GET':
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PlayerSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This is no longer used and has been replaced by player_api_view.
@api_view(['GET', 'PUT', 'DELETE'])
def player_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        player = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlayerSerializer(snippet, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        player.delete()
        return HttpResponse(status=204)


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



