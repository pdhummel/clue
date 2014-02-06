from django.db import models
from constants import CHARACTER_CHOICES, WEAPON_CHOICES, ROOM_CHOICES
from clue.models import Game, Player, PlayerCard

class GameSuggestion(models.Model):
    game_player = models.ForeignKey(GamePlayer)
    character = models.CharField(max_length=2, choices=CHARACTER_CHOICES)
    weapon = models.CharField(max_length=2, choices=WEAPON_CHOICES)
    room = models.CharField(max_length=2, choices=ROOM_CHOICES)
    evidence_revealed = card = models.ForeignKey(PlayerCard)

