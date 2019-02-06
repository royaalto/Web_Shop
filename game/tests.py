from django.test import TestCase, RequestFactory
import unittest
from django.db import models
from game.models import Game
from django.contrib.auth.models import User, Group




class GameModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        self.factory = RequestFactory()

    ''
    def _add_game(self,number=1):
        for i in range(number):
            game = Game()
            game.name ='name%d'%(i)
            game.description = 'description%d' % (i)
            game.url = 'https://notexisturl%d.fi' % (i)
            game.save()
    ''

    def test_product_creation(self):
        p = Game(owner=self.user, name='name', description='desc', url="http://url.fi",price=2.30,available=True)
        p.save()
        p = Game.objects.get(pk=p.pk)
        self.assertEquals(p.name, 'name', "Testing name")
        self.assertEquals(p.url,"http://url.fi","Testing URL")
        self.assertEquals(p.owner.username, self.user.username, "Testing owner of the game")



    def codetosetmanually(self):
        from game.models import Game
        from django.contrib.auth.models import User
        user = User.objects.get(pk=1)
        p = Game(owner=user, name='No Game', description='desc', url="http://url.fi",price=2.30,available=True)
        p.save()