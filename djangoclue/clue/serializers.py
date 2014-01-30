from django.forms import widgets
from rest_framework import serializers
from clue.models import Player, Game, GamePiece, Space


class PlayerSerializer1(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    name = serializers.CharField(max_length=50)
    is_human = serializers.BooleanField(default=True)
    gender = serializers.CharField(max_length=6, blank=True)
    games_played = serializers.IntegerField(default=0)
    games_won = serializers.IntegerField(default=0)
    
    def restore_object(self, attrs, instance=None):
        """
        Create or update a new Player instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.name)
            instance.is_human = attrs.get('is_human', instance.is_human)
            instance.gender = attrs.get('gender', instance.gender)
            return instance

        # Create new instance
        return Player(**attrs)
        
class PlayerSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Player
        fields = ('id', 'name', 'is_human', 'gender', 'games_played', 'games_won')


class GameSerializer(serializers.ModelSerializer):
    game_pieces = serializers.SerializerMethodField('get_game_pieces')

    def get_game_pieces(self, obj):
        return reverse('game_piece_list', 
               args=[obj.pk], request=self.context['request'])
               
    class Meta:
        model = Game
        fields = ('id', 'name', 'game_state', 'current_turn', 'last_die_roll', 
                  'suggested_character', 'suggested_weapon', 'suggested_room')

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
        
