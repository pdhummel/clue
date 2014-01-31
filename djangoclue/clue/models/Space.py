from django.db import models
from constants import DIRECTION_CHOICES, ROOM_CHOICES


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

    class Meta:
        app_label = 'clue'
