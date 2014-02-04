import random
from django.db import models
from constants import CHARACTER_CHOICES, WEAPON_CHOICES, ROOM_CHOICES
from GameBox import GameBox

class Game(models.Model):
    name = models.CharField(max_length=50)
    game_state = models.CharField(max_length=50, default='forming', null=True)
    current_turn = models.IntegerField(default=0)           # turns start with 1
    pending_evidence_player_turn = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)    
    secret_character = models.CharField(max_length=2, choices=CHARACTER_CHOICES, blank=True)
    secret_weapon = models.CharField(max_length=2, choices=WEAPON_CHOICES, blank=True)
    secret_room = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)
    suggested_character = models.CharField(max_length=2, choices=CHARACTER_CHOICES, blank=True)
    suggested_weapon = models.CharField(max_length=2, choices=WEAPON_CHOICES, blank=True)
    suggested_room = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)    
    end_time = models.DateTimeField(blank=True,null=True)
    last_die_roll = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.players = []   # game_player
        self.pieces = {}
      
    def add_player(self, player, character):
        self._open_game()        
        # TODO:  validate the game state
        from GamePlayer import GamePlayer
        if character not in self.pieces.keys():
            self._place_pieces()
        piece = self.pieces[character]           
        gp = GamePlayer.objects.create(game=self, player=player, piece=piece)
        self.players.append(gp)

    def start_game(self):
        self._open_game()        
        # TODO:  validate that we have enough players
        # TODO:  validate the game state
        self.game_state = "starting"
        self.save()
        self._set_turn_order()
        self._deal_cards()
        self.current_turn = 1
        self.game_state = "in_progress"
        self.save()
        
        
    def roll_die(self):
        # TODO:  validate the game state and whether the die has already been rolled
        import random
        die = [1,2,3,4,5,6]
        random.shuffle(die)
        self.last_die_roll = die[0]
        self.save()
        return die[0]
    
    def make_accusation(self, player, character, weapon, room):
        got_it_right = False
        if character == self.secret_character and \
           weapon == self.secret_weapon and \
           room == self.secret_room:
               got_it_right = True
        if got_it_right:
            # TODO:  player won game and game over
            pass
        else:
            # TODO:  player lost game and is out of the game
            pass
        return got_it_right
    
    # turns start with 1
    def end_turn(self, player):
        # TODO:  validate the player
        next_turn = self.current_turn + 1
        if next_turn > len(self.players):
            next_turn = 1
        self.current_turn = next_turn
        self.save()
    
    def gather_evidence(self, character, weapon, room):
        # TODO:  get evidence from all players sorted by turn.  The evidence for 
        # the player to the left of the current player should be first.
        pass
    
    
    def _open_game(self):
        from GamePiece import GamePiece
        from GamePlayer import GamePlayer
        if len(self.pieces) == 0:
            for gp in GamePiece.objects.filter(game=self):
                self.pieces[gp.character] = gp
        if len(self.players) == 0:
            for gp in GamePlayer.objects.filter(game=self):
                self.players.append(gp)
        
    
    def _open_game_box(self):
        if (not hasattr(self, 'game_box')) or (not self.game_box):
            self.game_box = GameBox()
            self.game_box.open()
            if len(self.game_box.cards) == 0:
                self.game_box.create()
    
    def _place_pieces(self):
        from GamePiece import GamePiece
        self._open_game_box()
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[0][0], space=self.game_box.board[0][1])
        self.pieces[gp.character] = gp
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[1][0], space=self.game_box.board[0][2])
        self.pieces[gp.character] = gp
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[2][0], space=self.game_box.board[0][3])
        self.pieces[gp.character] = gp
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[3][0], space=self.game_box.board[0][4])
        self.pieces[gp.character] = gp
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[4][0], space=self.game_box.board[0][5])
        self.pieces[gp.character] = gp
        gp = GamePiece.objects.create(game=self, character=CHARACTER_CHOICES[5][0], space=self.game_box.board[0][6])
        self.pieces[gp.character] = gp


        
            
    def _set_turn_order(self):
        turn_order = 1
        for player in self.players:
            player.turn_order = turn_order
            player.save()
            turn_order = turn_order + 1
        
    
    def _deal_cards(self):
        self._open_game_box()
        # Pick the killer, weapon, and room
        weapons = list(WEAPON_CHOICES)
        random.shuffle(weapons)
        self.secret_weapon = weapons[0][0]
        characters = list(CHARACTER_CHOICES)
        random.shuffle(characters)
        self.secret_character = characters[0][0]
        rooms = list(ROOM_CHOICES)
        self.secret_room = rooms[0][0]
        self.save()
        
        # Get the remaining cards in the deck and shuffle them
        cards = []
        for weapon in weapons[1:]:
            card = self.game_box.cards[weapon[0]]
            cards.append(card)
        for room in rooms[1:]:
            card = self.game_box.cards[room[0]]
            cards.append(card)
        for character in characters[1:]:
            card = self.game_box.cards[character[0]]
            cards.append(card)
        random.shuffle(cards)
        
        # Deal the cards
        from PlayerCard import PlayerCard
        player_num = 0
        for card in cards:
            PlayerCard.objects.create(player=self.players[player_num], card=card)
            player_num = player_num + 1
            if player_num >= len(self.players):
                player_num = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'current_turn=' + str(self.current_turn) + '\nsecret_weapon=' + \
            self.secret_weapon + ', secret_room=' + self.secret_room + \
            ', secret_character=' + self.secret_character + \
            '\nplayers='  + str(self.players) + '\npieces=' + str(self.pieces)
        return s

    class Meta:
        app_label = 'clue'
        
        
