from django.db import models
from django.contrib.auth.models import User
from game.models import Game


class Collection(models.Model):
    '''
    Models that tells what games a user owns.
    '''

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)


    def addCart(user, cart):
        '''
        Add all games in the cart to the user

        :param user: user object
        :param cart: cart object
        :return: True, if everything added
        '''
        try:
            for item in cart.item.all():
                collection = Collection(user=user, game=item.game)
                collection.save()
            return True
        except:
            return False


    def isUserOwning(user, game):
        '''
        If user owns the game, true is returned

        :param user:
        :param game:
        :return: boolen
        '''
        result = Collection.objects.filter(user=user,game=game)
        if(len(result) > 0):
            return True
        return False