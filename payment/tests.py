from django.test import TestCase, RequestFactory
from payment.models import *
from game.models import Game
from django.contrib.auth.models import User

from decimal import *


# Create your tests here.



class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart(user=self.user)
        self.factory = RequestFactory()

    def _add_game(self,number=1):
        for i in range(number):
            game = Game()
            game.owner = self.user
            game.name = 'name%d'%(i)
            game.description = 'description%d' % (i)
            game.url = 'https://notexisturl%d.fi' % (i)
            game.price = 1.0
            game.save()


    def test_cart_creation(self):
        cart = Cart(user=self.user)
        self.assertEquals(cart.user.username, 'testuser', "the owner of thr cart is testuser")
        self.assertEquals(cart.activity, True, 'default activity is true')
        self.assertEquals(cart.total_price, 0.0, "total price = 0.0")
        self.assertEquals(cart.total_qty, 0, "quantity = 0")
        # self.assertEquals(1, 1, "comment")


    def test_item_creation(self):

        self._add_game()
        item = Item(game=Game.objects.get(pk=1))
        item.save()
        self.assertEquals(Item.objects.get(pk=1).subtotal, 1.0, "subtotal should be 1.0")

        item = Item(game=Game.objects.get(pk=1))
        item.qty = 3
        item.save()
        self.assertEquals(Item.objects.get(pk=2).subtotal, 3.0, "subtotal should be 1.0")


    def test_cart_add_item(self):
        self.cart.save()
        self._add_game()
        self.assertEquals(self.cart.total_qty, 0, "total qty is 0 at start")

        item = Item(game=Game.objects.get(pk=1))
        item.save()
        self.cart.item.add(item)
        self.cart.save()

        self.assertEquals(self.cart.item.all()[0].game.name, 'name0', "first item")
        self.assertEquals(self.cart.total_qty, 1, "after adding first item, total_qty is 1")
        self.assertEquals(self.cart.total_price, 1.00, "total price is 1.0")

        game = Game.objects.get(pk=1)
        game.price = 1.4
        game.save()
        item = Item(game=game)
        item.qty = 2
        item.save()
        self.cart.item.add(item)
        self.cart.save()
        self.assertEquals(self.cart.total_qty, 3, "after adding second item, total_qty is 3")
        self.assertEquals(self.cart.total_price, Decimal("3.8"), "total price is 3.8")


    def test_cart_delete_item(self):
        self.cart.save()
        self._add_game(5)

        for game in Game.objects.all():
            item = Item(game=game)
            item.save()
            self.cart.item.add(item)
        self.cart.save()

        self.assertEquals(self.cart.total_qty, 5, "setup, total_qty is 5")
        self.assertEquals(self.cart.total_price, Decimal("5.0"), "total price is 5.0")

        item3 = Item.objects.get(pk=3)
        item3.delete()
        self.cart.save()

        self.assertEquals(self.cart.total_qty, 4, "setup, total_qty is 4")
        self.assertEquals(self.cart.total_price, Decimal("4.0"), "total price is 4.0")


    def test_get_game_list(self):
        self.cart.save()
        self._add_game(5)

        for game in Game.objects.all():
            item = Item(game=game)
            item.save()
            self.cart.item.add(item)
        self.cart.save()

        self.assertEquals(self.cart.total_qty, 5, "setup, total_qty is 5")
        self.assertEquals(self.cart.total_price, Decimal("5.0"), "total price is 5.0")

        item3 = Item.objects.get(pk=3)
        item3.delete()
        self.cart.save()

        gameList = [Game.objects.get(pk=1),Game.objects.get(pk=2),
                    Game.objects.get(pk=4),Game.objects.get(pk=5)]

        self.assertEquals(self.cart.getGameList(), gameList ,"the list")


class TransactionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart(user=self.user)
        self.factory = RequestFactory()

    def _add_game(self,number=1):
        for i in range(number):
            game = Game()
            game.owner = self.user
            game.name = 'name%d'%(i)
            game.description = 'description%d' % (i)
            game.url = 'https://notexisturl%d.fi' % (i)
            game.price = 1.0
            game.save()

    def test_buyCart(self):
        self.cart.save()
        self._add_game(5)

        # Add games to the cart.
        for game in Game.objects.all():
            item = Item(game=game)
            item.save()
            self.cart.item.add(item)
        self.cart.save()

        # Buy the content of the cart
        self.cart.buyCart()

        list_of_games = []
        for trans in Transaction.objects.all():
            list_of_games.append(trans.game)

        self.assertEquals(self.cart.getGameList(), list_of_games, "the test")
        self.assertEquals(self.cart.activity, False, "activity should be false afte buying")


    def test_validata_prices(self):
        self.cart.save()
        self._add_game(5)

        # Add games to the cart.
        for game in Game.objects.all():
            item = Item(game=game)
            item.save()
            self.cart.item.add(item)
        self.cart.save()


        #change price of a game
        item3 = Game.objects.get(pk=3)
        item3.price = Decimal("60.90")
        item3.save()
        self.cart.save()

        self.assertEquals(self.cart.total_qty, 5, "setup, total_qty is 5")
        self.assertEquals(self.cart.total_price, Decimal("5.0"), "total price is 5.0")

        self.assertEquals((Game.objects.get(pk=3)).price, Decimal("60.90"), "Item 3 price is changed to 60.90")

        self.assertEquals(self.cart.validateItemPrices(),False,"Should be false")


class ItemInCartTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart(user=self.user)
        self.factory = RequestFactory()

    def _add_game(self,number=1):
        for i in range(number):
            game = Game()
            game.owner = self.user
            game.name = 'name%d'%(i)
            game.description = 'description%d' % (i)
            game.url = 'https://notexisturl%d.fi' % (i)
            game.price = 1.0
            game.save()

    def test_game_in_cart(self):
        #Set up
        self.cart.save()
        self._add_game(5)

        for game in Game.objects.all():
            item = Item(game=game)
            item.save()
            self.cart.item.add(item)
        self.cart.save()

        self.assertEquals(self.cart.total_qty, 5, "setup, total_qty is 5")
        self.assertEquals(self.cart.total_price, Decimal("5.0"), "total price is 5.0")

        # delete one item from cart
        item3 = Item.objects.get(pk=3)
        item3.delete()
        self.cart.save()

        # test the function
        game3 = Game.objects.get(pk=3)
        resultGame3 = Cart.isItemInCart(user=self.user,game=game3)

        game1 = Game.objects.get(pk=1)
        resultGame1 = Cart.isItemInCart(user=self.user, game=game1)


        self.assertEquals(resultGame3, False ,"Game 3 not in cart")
        self.assertEquals(resultGame1, True , "Game 1 not in cart")