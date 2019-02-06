from django.shortcuts import render
from game.models import Game
from collection.models import Collection

def collection_view(request):
    if request.user.is_authenticated:
        if request.user.groups.get(name='Player'):
            context = {}
            collection = Collection.objects.filter(user=request.user).order_by('game__name')
            game_collection = []

            # Add game object to the game_collection,
            # if user have multiple of the same game, increase count
            for colle in collection:
                if colle.game in game_collection:
                    idx = game_collection.index(colle.game)
                    game_collection[idx].count += 1
                else:
                    colle.game.count=1
                    game_collection.append(colle.game)

            context['collection']= game_collection
            return render(request, "collection/collection.html",context)
    else:
        return render(request, "403.html")

def inventory_view(request):
    if request.user.is_authenticated:
        if request.user.groups.get(name='Developer'):
            game_list = Game.objects.filter(owner=request.user)
            context = {
                "inventory": game_list
            }
            return render(request, "collection/inventory.html",context)
    return render(request, "403.html")
