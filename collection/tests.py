from django.test import TestCase
from collection.models import *
from payment.models import *
from game.models import Game
from django.contrib.auth.models import User


class CollectionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart(user=self.user)


    def _add_game(self, number=1):
        for i in range(number):
            game = Game()
            game.owner = self.user
            game.name = 'name%d' % (i)
            game.description = 'description%d' % (i)
            game.url = 'https://notexisturl%d.fi' % (i)
            game.price = Decimal("1."+str(i))
            game.save()




    def test_add_cart(self):
        '''
        Test method addCart() and method isUserOwning().
        '''
        # Set up cart
        self.cart.save()
        self._add_game(5)

        # Add some game to the cart
        item = Item(game=Game.objects.get(pk=2))
        item.save()
        self.cart.item.add(item)

        item = Item(game=Game.objects.get(pk=4))
        item.save()
        self.cart.item.add(item)



        # Add cart games to the table
        Collection.addCart(user=self.user, cart=self.cart)

        # Check result
        self.assertEquals(Collection.isUserOwning(self.user, Game.objects.get(pk=1)), False, "User do not own game 1")
        self.assertEquals(Collection.isUserOwning(self.user, Game.objects.get(pk=2)), True, "User owns game 2")
        self.assertEquals(Collection.isUserOwning(self.user, Game.objects.get(pk=3)), False, "User do not own game 3")
        self.assertEquals(Collection.isUserOwning(self.user, Game.objects.get(pk=4)), True, "User owns game 4")