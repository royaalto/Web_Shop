from django.db import models
from django.contrib.auth.models import User
from game.models import Game
from decimal import *
from collection.models import Collection


class Item(models.Model):
    '''
    Model for items
    '''
    #cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)

    def update(self):
        self.subtotal = self.game.price * self.qty

    def save(self, *args, **kwargs):
        self.update()
        super(Item, self).save(*args, **kwargs)

class Cart(models.Model):
    '''
    Model for Cart
    '''
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    activity = models.BooleanField(default=True)
    total_price = models.DecimalField(default=0.0,max_digits=6,decimal_places=2)
    total_qty = models.IntegerField(default=0)
    item = models.ManyToManyField(
        Item,
        verbose_name='item',
        blank=True,
    )

    def _update(self):
        try:
            qtys=[]
            for item in self.item.all():
                qtys.append(item.qty)
            self.total_qty = sum(qtys)
            subtotals=[]
            for item in self.item.all():
                subtotals.append(item.subtotal)
            self.total_price = sum(subtotals)
        except ValueError:
            # self.item is empty so everything is default
            pass

    def save(self, *args, **kwargs):
        self._update()
        super(Cart, self).save(*args, **kwargs)


    def getGameList(self):
        '''
        Get a list of games that are in the cart.

        :return: List of Game-objects
        '''
        gameList = []
        for item in self.item.all():
            gameList.append(item.game)

        return gameList


    def validateItemPrices(self):
        '''
        Validate that game prices are still same.

        :return: True if prices are the same.
        '''

        for item in self.item.all():
            if not(item.game.price == item.subtotal / item.qty):
                return False
        return True

    def buyCart(self):
        '''
        Create transaction for every game in the cart.
        Should be called after validateItemPrices().

        :return: True if set transaction success
        '''
        try:
            gameList = self.getGameList()
            for game in gameList:
                transaction = Transaction(buyer=self.user,game=game,price=game.price)
                transaction.save()
                game.revenue += game.price
                game.sold_qty += 1
                game.save()
            self.activity = False
            self.save()
            Collection.addCart(user=self.user, cart=self)
            Cart.getActiveCart(user=self.user)
            return True
        except:
            return False


    def getActiveCart(user):
        '''
        Get active cart of current user. Create new if not found.

        :return: cart
        '''

        list = Cart.objects.filter(user=user,activity=True)
        if(len(list)==1):
            return list[0]
        elif (len(list) == 0):
            # If no active cart, create new one.
            cart = Cart(user=user)
            cart.save()
            return cart
        else:
            if(len(list)>1):
                for i in list:
                    i.activity = False
                    i.save()
            return None


    def getCartItemCount(user):
        '''
        Get item count in the cart of user. If user is anonymous user, return None

        :return: int, number of items in the cart
        '''

        if(user.is_authenticated):
            return Cart.getActiveCart(user).total_qty
        return None


    def isItemInCart(user,game):
        '''
        Return true if user have the game in cart, else False.

        :param game_id:
        :return: boolean
        '''
        cart = Cart.getActiveCart(user)
        if game in cart.getGameList():
            return True
        return False



class Transaction(models.Model):
    '''
    Model for transaction
    '''
    buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)





