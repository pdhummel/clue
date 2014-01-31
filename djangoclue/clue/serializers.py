from django.forms import widgets
from rest_framework import serializers
from clue.models import Player, Game, GamePiece, Space, GamePlayer, \
                        Card, PlayerCard



class PlayerSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Player
        fields = ('id', 'name', 'is_human', 'gender', 'games_played', 'games_won')


class GameListSerializer(serializers.ModelSerializer):
    def validate_game_state(self, attrs, source):
        "Set a default game_state."
        attrs[source] = "forming"
        return attrs    
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_state', 'start_time', 'end_time')

class GameSerializer(serializers.ModelSerializer):
    game_pieces = serializers.SerializerMethodField('get_game_pieces')

    def get_game_pieces(self, obj):
        game_pieces = []
        for gp in GamePiece.objects.filter(game__id=obj.pk):
            game_piece = GamePieceSerializer(gp).data  
            game_pieces.append(game_piece)
        return game_pieces
               
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_state', 'current_turn', 'last_die_roll', 
                  'suggested_character', 'suggested_weapon', 'suggested_room', 
                  'game_pieces')

class GameSecretSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Game
        fields = ('id', 'secret_character', 'secret_weapon', 'secret_room')

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ('id', 'x', 'y', 'room', 'is_blocked', 'door_direction', 'door_to_room')


class GamePieceSerializer(serializers.ModelSerializer):
    space = SpaceSerializer(source='space')    
    class Meta:
        model = GamePiece
        fields = ('id', 'character', 'space', 'room')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'description', 'type')

        
class GamePlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source='player')
    piece = GamePieceSerializer(source='piece')
    
    cards = serializers.SerializerMethodField('get_player_cards')
    actions_allowed = serializers.SerializerMethodField('get_allowed_actions')
    
    def get_player_cards(self, obj):
        cards = []
        for pc in PlayerCard.objects.filter(player__id=obj.pk):
            card = CardSerializer(pc.card).data  
            cards.append(card)
        return cards
    
    def get_allowed_actions(self, obj):
        actions = obj.get_actions_allowed()
        return actions    
    
    class Meta:
        model = GamePlayer
        fields = ('id', 'player', 'piece', 'turn_order', 'is_game_organizer', 
                  'cards', 'actions_allowed')

class GamePlayerListSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(source='player')
    piece = GamePieceSerializer(source='piece')
    class Meta:
        model = GamePlayer
        fields = ('id', 'player', 'piece', 'turn_order', 'is_game_organizer')
