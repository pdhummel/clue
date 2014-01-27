'''
Created on Jul 5, 2013

@author: phummel
'''
import random
from django.db import models


CHARACTER_CHOICES = (
    ('PP', 'Professor Plum'),
    ('MP', 'Mrs. Peacock'),
    ('MS', 'Miss Scarlet'),
    ('CM', 'Colonel Mustard'),
    ('MG', 'Mr. Green'),
    ('MW', 'Mrs. White'),
)

WEAPON_CHOICES = (
    ('Kn', 'Knife'),
    ('Wr', 'Wrench'),
    ('LP', 'Lead Pipe'),
    ('Re', 'Revolver'),
    ('Ro', 'Rope'),
    ('Ca', 'Candlestick'),
)

ROOM_CHOICES = (
    ('St', 'Study'),
    ('Ha', 'Hall'),
    ('Lo', 'Lounge'),
    ('Li', 'Library'),
    ('DR', 'Dining Room'),
    ('BR', 'Billard Room'),
    ('Ba', 'Ballroom'),
    ('Ki', 'Kitchen'),
    ('Co', 'Conservatory'),
)

CARD_TYPE_CHOICES = (
    ('W', 'Weapon'),
    ('R', 'Room'),
    ('C', 'Character'),
)

CARD_CHOICES = sum([CHARACTER_CHOICES, WEAPON_CHOICES, ROOM_CHOICES], ())

DIRECTION_CHOICES = (
    ('U', 'up'),
    ('D', 'down'),
    ('L', 'left'),
    ('R', 'right'),
)



class GameBox():
    def __init__(self):
        self.weapons = list(WEAPON_CHOICES)

    def create(self):
        self.cards = Card.create_deck()
        self.board = Space.create_board()

    def open(self):
        self.cards = {}
        for card in Card.objects.filter():
            self.cards[card.description] = card
        self.board = [[0 for x in xrange(24)] for x in xrange(25)]
        for space in Space.objects.filter():
            self.board[space.x][space.y] = space

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'weapons=' + self.weapons + ', cards=' + self.cards + \
            ', board=' + str(self.board)
        return s


class Card(models.Model):
    description = models.CharField(max_length=2, choices=CARD_CHOICES)
    type = models.CharField(max_length=1, choices=CARD_TYPE_CHOICES)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'description=' + self.description + ', type=' + self.type
        return s
    
    @staticmethod
    def create_deck():
        cards = {}
        weapons = list(WEAPON_CHOICES)
        characters = list(CHARACTER_CHOICES)
        rooms = list(ROOM_CHOICES)
        
        for weapon in weapons:
            card = Card.objects.create(type=CARD_TYPE_CHOICES[0][0], description=weapon[0])
            cards[card.description] = card
        for room in rooms:
            card = Card.objects.create(type=CARD_TYPE_CHOICES[1][0], description=room[0])
            cards[card.description] = card
        for character in characters:
            card = Card.objects.create(type=CARD_TYPE_CHOICES[2][0], description=character[0])
            cards[card.description] = card
        return cards
    

class Space(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    is_blocked = models.BooleanField(default=False)
    room  = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)
    door_direction  = models.CharField(max_length=1, choices=DIRECTION_CHOICES, blank=True)
    door_to_room  = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'x=' + str(self.x) + ',y=' + str(self.y) + ', blocked=' + \
            str(self.is_blocked) + ', room=' + self.room + ', door=' + \
            self.door_to_room
        return s

    @staticmethod
    def create_board():
        rows = []
        # 24x25
        #            012345678901234567890123
        rows.append('1111111ox222222xox333333') # 0
        rows.append('1111111oo222222oo3333333') # 1
        rows.append('1111111oo222222oo3333333') # 2
        rows.append('1111111oo222222oo3333333') # 3
        rows.append('xoooooUoR222222oo3333333') # 4
        rows.append('ooooooooo222222oo3333333') # 5
        rows.append('x44444ooo222222ooUooooox') # 6
        rows.append('4444444ooooUUooooooooooo') # 7
        rows.append('4444444LoxxxxxoooDooooox') # 8
        rows.append('4444444ooxxxxxoo55555555') # 9
        rows.append('444444oooxxxxxoo55555555') # 10
        rows.append('xDoUoooooxxxxxoo55555555') # 11
        rows.append('666666oooxxxxxoR55555555') # 12
        rows.append('666666oooxxxxxoo55555555') # 13
        rows.append('666666oooxxxxxoo55555555') # 14
        rows.append('666666Loooooooooooo55555') # 15
        rows.append('666666oooDooooDoooooooox') # 16
        rows.append('xooooooo77777777oooDoooo') # 17
        rows.append('oooooooo77777777oo88888x') # 18
        rows.append('x9999LoR77777777Lo888888') # 19
        rows.append('999999oo77777777oo888888') # 20
        rows.append('999999oo77777777oo888888') # 21
        rows.append('999999oo77777777oo888888') # 22
        rows.append('999999xooo7777ooox888888') # 23
        rows.append('xxxxxxxxxo7777oxxxxxxxxx') # 24
        
        room_map = {
            '1': ROOM_CHOICES[0], # study
            '2': ROOM_CHOICES[1], # hall
            '3': ROOM_CHOICES[2], # lounge
            '4': ROOM_CHOICES[3], # library
            '5': ROOM_CHOICES[4], # dining room
            '6': ROOM_CHOICES[5], # billard room
            '7': ROOM_CHOICES[6], # ballroom
            '8': ROOM_CHOICES[7], # kitchen
            '9': ROOM_CHOICES[8], # conservatory
        }
        
        all_doors = []
        spaces = [[0 for x in xrange(24)] for x in xrange(25)] 
        row_num = 0
        for row in rows:
            col_num = 0
            for char in row:
                space = Space.objects.create(x=row_num,y=col_num)
                if char in '123456789':
                    space.room = room_map[char][0]
                elif char in 'UDLR':
                    space.door_direction = char
                    all_doors.append(space)
                elif char in 'xX':
                    space.is_blocked = True
                spaces[row_num][col_num] = space
                space.save()
                col_num = col_num + 1
            row_num = row_num + 1

        for door in all_doors:
            connecting_space = None
            if door.door_direction == 'U':
                connecting_space = spaces[door.y-1][door.x]
            elif door.door_direction == 'D':
                connecting_space = spaces[door.y+1][door.x]
            elif door.door_direction == 'R':
                connecting_space = spaces[door.y][door.x+1]
            elif door.door_direction == 'L':
                connecting_space = spaces[door.y][door.x-1]
            door.door_to_room = connecting_space.room
            door.save()
        return spaces


        


class Player(models.Model):
    name = models.CharField(max_length=50)
    is_human = models.BooleanField(default=True)
    gender = models.CharField(max_length=6, blank=True)
    games_played = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'name=' + self.name
        return s




    

class Game(models.Model):
    name = models.CharField(max_length=50)
    current_turn = models.IntegerField(default=0)
    start_time = models.DateTimeField(auto_now_add=True)    
    secret_character = models.CharField(max_length=2, choices=CHARACTER_CHOICES, blank=True)
    secret_weapon = models.CharField(max_length=2, choices=WEAPON_CHOICES, blank=True)
    secret_room = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)
    end_time = models.DateTimeField(blank=True)

    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.players = []
        self.pieces = {}
      
    def add_player(self, player, character):
        if character not in self.pieces.keys():
            self._place_pieces()
        piece = self.pieces[character]           
        gp = GamePlayer.objects.create(game=self, player=player, piece=piece)
        self.players.append(gp)
        

    
    def _place_pieces(self):
        self.game_box = GameBox()
        self.game_box.open()           
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


    def start_game(self):
        # TODO:  validate that we have enough players
        self._set_turn_order()
        self._deal_cards()
        
            
    def _set_turn_order(self):
        turn_order = 0
        for player in self.players:
            player.turn_order = turn_order
            player.save()
            turn_order = turn_order + 1
        
    
    def _deal_cards(self):
        # Pick the killer, weapon, and room
        weapons = list(WEAPON_CHOICES)
        random.shuffle(weapons)
        self.secret_weapon = weapons[0][0]
        characters = list(CHARACTER_CHOICES)
        random.shuffle(characters)
        self.secret_character = characters[0][0]
        rooms = list(ROOM_CHOICES)
        self.secret_room = rooms[0][0]
        
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


class GamePiece(models.Model):
    game = models.ForeignKey(Game)
    character = models.CharField(max_length=2, choices=CHARACTER_CHOICES)
    space = models.ForeignKey(Space, blank=True)
    room  = models.CharField(max_length=2, choices=ROOM_CHOICES, blank=True)    

        
    def move_piece(self, die_count, row, col, room=None):
        is_ok = False

        if room:
            # TODO:  validate die roll and movement
            # TODO: validate room
            is_ok = True
        elif row and col and room == None:
            #TODO:  validate die roll and movement
            is_ok = True
            if row != self.y or col != self.x:
                new_space = Space.objects.get(x=col, y=row)
                try:
                    GamePiece.objects.get(space=new_space)
                    is_ok = False
                except:
                    is_ok = True
                if new_space.is_blocked:
                    is_ok = False                    

        if is_ok:
            self.place_piece(row, col, room)
        return is_ok


    def place_piece(self, row, col, room):
        if room:
            self.room = room
            self.space = None
        else:
            self.room = None
            new_space = Space.objects.get(x=col, y=row)
            self.space = new_space
        self.save()
  
        
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'character=' + self.character +  \
            ', space=' + str(self.space) + ', room=' + self.room
        return s


    
class GamePlayer(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    piece = models.ForeignKey(GamePiece, blank=True)
    turn_order = models.IntegerField(default=0)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'player=' + str(self.player) +  \
            ', piece=' + str(self.piece) + ', turn_order=' + str(self.turn_order)
        return s

  
class PlayerCard(models.Model):
    player = models.ForeignKey(GamePlayer)
    card = models.ForeignKey(Card)
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = 'player=' + str(self.player) +  \
            ', card=' + str(self.card)
        return s
    