from constants import WEAPON_CHOICES
from Card import Card
from Space import Space

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
        s = 'weapons=' + str(self.weapons) + ', cards=' + str(self.cards) + \
            ', board=' + str(self.board)
        return s
