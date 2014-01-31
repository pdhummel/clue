from django.db import models
from GamePlayer import GamePlayer
from Card import Card

class PlayerCard(models.Model):
    player = models.ForeignKey(GamePlayer)
    card = models.ForeignKey(Card)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'player=' + str(self.player) +  \
            ', card=' + str(self.card)
        return s

    class Meta:
        app_label = 'clue'