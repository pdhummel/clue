from django.db import models

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

    class Meta:
        app_label = 'clue'