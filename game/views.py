from django.shortcuts import render, redirect, get_object_or_404
from game.models import Game, Category
from .forms import *
from django.core.paginator import Paginator,Page
from payment.models import *
from django.db.models import Q
from django.views.generic import ListView
from payment.models import Transaction
from collection.models import Collection


def decimalToPriceTag(decimal):
    return str(decimal)+'€'

def new_edit_view(request):
    if request.user.groups.get(name='Developer'):
        context = {}
        context['form_action'] = ''
        if request.method == 'POST':
            form = GameForm(request.POST, request.FILES)#put the request form into gameform
            #if the form is valid
            if form.is_valid():
                game= form.save(commit=False)
                game.owner = request.user
                categories = form.cleaned_data.get('category')
                game.save()
                for i in range(len(categories)):
                    game.category.add(categories[i])
                game.save()
                return redirect('/inventory')
            else:
                context['message']= 'alert-danger'
        else:
            form = GameForm()
        context['form'] = form
        return render(request, "game/edit.html", context)
    return render(request, "403.html")


def play_view(request,id):
    context={}
    if request.user.is_authenticated:
        game = get_object_or_404(Game,pk=id)##from the model find the id corresponding game
        if (Collection.isUserOwning(request.user, game)):
            context['game']=game
            return render(request,"game/play.html",context)
        if request.user==game.owner:#develop has the game.owenership so they can play the game
            context['game']=game
            return render(request,"game/play.html",context)
    return render(request,"403.html")


def description(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    context = {}

    # If game not available
    if not (game.available):
        if (request.user.is_authenticated and
            (Collection.isUserOwning(user=request.user, game=game) or
            game.owner == request.user)
        ):
            context['extra_message'] = "Game is not in sale anymore."

        else:
            return render(request, '404.html')

    # if game available or already bought
    if (request.user.is_authenticated):
        # If user have bought the game
        if(Collection.isUserOwning(user=request.user,game=game)):
            owned = True
        # User is developer and owns the game
        elif(game.owner == request.user):
            owned = True
        # User is developer but not owner
        elif (request.user.groups.all()[0].name == 'Developer'):
            owned = -1
        else:
            owned = False
        in_cart = Cart.isItemInCart(request.user,game)
    else:
        owned = None
        in_cart= False

    game.priceTag = decimalToPriceTag(game.price)
    categories = game.category.all()

    context['game'] = game
    context['owned'] = owned           # True if player and bought or owner. False if not bought. -1 if other developer.
    context['in_cart'] = in_cart       # Shows if the game is already added to the cart
    context['categories'] = categories # All categories of the game

    return render(request,"game/description.html",context)


def category(request, pk):
    error_msg = 'There is no game!'
    cate = get_object_or_404(Category, pk=pk)
    game_list = Game.objects.filter(category=cate).order_by('-name')
    game_list = game_list.filter(available=True)
    context = {'game_list': game_list,
               'category': cate.name,
               'error_msg': error_msg}
    return render(request, 'game/search.html', context)


def edit_view(request,game_id):
    if request.user.is_authenticated:
        user = request.user
        context = {}
        game=Game.objects.get(pk=game_id)

        # If user is not the owner of the game, -> 403
        if(game.owner != user):
            return render(request, "403.html")

        form = GameForm(instance=game)
        if request.method == 'POST':
            form = GameForm(request.POST, request.FILES, instance=game)
            if form.is_valid():
                form.save()
                return redirect('/inventory')
            else:
                context['message']= 'alert-danger'
        context['form'] = form
        return render(request, "game/edit.html", context)

    # User not logged in
    return render(request,"403.html")


def search(request):
    q = request.GET.get('q')
    error_msg = 'There is no game. Please try other keywords!'
    game_list = Game.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
    game_list = game_list.filter(available=True)
    context = {'error_msg': error_msg,
               'game_list': game_list}
    return render(request, 'game/search.html', context)

class IndexView(ListView):
    model = Game
    template_name = 'game/search.html'
    context_object_name = 'game_list'
    paginate_by = 9


def statistic_view(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if (request.user.is_authenticated):
        if(request.user == game.owner):
            game.priceTag = decimalToPriceTag(game.price)

            # Get 5 most recent transaction
            trans = Transaction.objects.filter(game = game).order_by('-date')[:5]
            categories = game.category.all()
            context = {
                'game': game,
                'trans':trans,
                'categories':categories
            }
            return render(request, "game/statistic.html", context)

    return render(request, "403.html")

