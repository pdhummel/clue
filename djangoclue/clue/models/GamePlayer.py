from django.db import models
from constants import GAME_STATE_ACTIONS
from Game import Game
from Player import Player
from GamePiece import GamePiece

class GamePlayer(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    piece = models.ForeignKey(GamePiece, blank=True)
    turn_order = models.IntegerField(default=0)
    is_game_organizer = models.BooleanField(default=False)    

    def get_my_cards(self):
        from PlayerCard import PlayerCard
        my_cards = []
        for card in PlayerCard.objects.filter(player=self):
            my_cards.append(card)
        return my_cards


    def is_current_player(self):
        if self.turn_order == self.game.current_turn:
            return True
        else:
            return False
    
    def get_actions_allowed(self):
        actions = []
        if self.game.game_state in GAME_STATE_ACTIONS:
            role_action_dict = GAME_STATE_ACTIONS[self.game.game_state]
            if "all" in role_action_dict:
                for action in role_action_dict["all"]:
                    actions.append(action)
            if self.is_game_organizer and "organizer" in role_action_dict:
                for action in role_action_dict["organizer"]:
                    actions.append(action)
            if self.is_current_player() and "current_player" in role_action_dict:
                for action in role_action_dict["current_player"]:
                    actions.append(action)
            if self.game.suggested_room and self.game.suggested_character and \
               self.game.suggested_weapon and \
               self.game.pending_evidence_player_turn == self.turn_order:
                actions.append("share_evidence")
        return actions
        
    def gather_evidence(self, character, weapon, room):
        from PlayerCard import PlayerCard
        evidence = []
        for card in PlayerCard.objects.filter(player=self):
            # card.description (CARD_CHOICES), card.type (CARD_TYPE_CHOICES)
            if card.description == character or \
               card.description == weapon or \
               card.description == room:
                evidence.append(card)
        return evidence

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'player=' + str(self.player) +  \
            ', piece=' + str(self.piece) + ', turn_order=' + str(self.turn_order)
        return s

    class Meta:
        app_label = 'clue'
