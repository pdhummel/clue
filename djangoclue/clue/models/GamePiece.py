from django.db import models
from constants import CHARACTER_CHOICES, ROOM_CHOICES
from Game import Game
from Space import Space


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
            if self.space and (row != self.space.y or col != self.space.x):
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
            ', space=' + str(self.space) + ', room=' + str(self.room)
        return s


    class Meta:
        app_label = 'clue'