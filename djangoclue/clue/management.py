import models
from django.dispatch import Signal
from django.db.models import signals
from clue.models import GameBox


def initialize_gamebox(sender, **kwargs):
    # initialize the gamebox
    print "initializing the GameBox"
    game_box = GameBox()
    game_box.open()
    if len(game_box.cards) == 0:
        game_box.create()


signals.post_syncdb.connect(initialize_gamebox, sender=models)