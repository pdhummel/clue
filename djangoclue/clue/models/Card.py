from django.db import models
from constants import WEAPON_CHOICES, CARD_CHOICES, CARD_TYPE_CHOICES, \
    CHARACTER_CHOICES, ROOM_CHOICES

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
    
    class Meta:
        app_label = 'clue'
