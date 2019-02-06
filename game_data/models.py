from django.db import models
from django.contrib.auth.models import User
from game.models import Game
# Create your models here.



class Score(models.Model):
    score = models.PositiveIntegerField()
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)


    def get_highest_score_each_game(a=0):
        all = Score.objects.all()

        keys = []
        high_scores = []
        for s in all:
            if s.game.name in keys:
                idx = keys.index(s.game.name)
                old = high_scores[idx]
                if (old.score < s.score):
                    high_scores[idx] = s
            else:
                keys.append(s.game.name)
                high_scores.append(s)

        return high_scores


class Game_save(models.Model):
    data = models.TextField(null=True,blank=True)
    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now=True)