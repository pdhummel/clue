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



# forming, starting, in_progress, ended
GAME_STATE_ACTIONS = {
    "forming": {"organizer": ["start_game"], "all": ["join_game"]},
    "starting": {},
    "in_progress": {
        "current_player": ["roll_die", "move", "make_suggestion", "make_accusation", "end_turn"],
        "organizer": ["end_game"],
        "all": ["view_cards", "view_notepad"]
    },
    "ended": {}
}
