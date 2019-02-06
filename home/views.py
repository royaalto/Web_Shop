from django.shortcuts import render
from game.models import Game
# Create your views here.


def home_view(request):
    game_list = Game.objects.filter(available=True).order_by('-id')[:3]
    context = {'game_list': game_list}
    return render(request, "home/home.html", context)


def error_404(request):
    return render(request,'404.html')

