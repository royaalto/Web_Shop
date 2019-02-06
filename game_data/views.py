from django.shortcuts import render
from django.http import JsonResponse
import json

from game_data.models import *
from game.models import Game


def score_board(request):
    context={}

    context['scores']=Score.get_highest_score_each_game()
    return render(request, "game_data/game_board.html", context)


def score_board_game(request,game_id):
    game = Game.objects.get(pk=game_id)
    if (game.score_board):
        # Get top 20 high score
        scores = Score.objects.filter(game=game).order_by('-score')[:20]
        context = {
            'scores': scores
        }
        return render(request, "game_data/game_board_game.html", context)
    return render(request, "404.html")


def post_score(request):
    if request.method == "POST" and request.is_ajax():
        return_data = {
            'message':False
        }
        post_data = request.POST
        message = json.loads(post_data['message'])
        messageType = message['messageType']


        if (messageType == "SCORE"):
            # Save new score
            game = Game.objects.get(pk=message['game_id'])
            score = Score(score=message['score'], game=game, user=request.user)
            score.save()

        elif (messageType == "SAVE"):
            # save game data to db
            json_str = json.dumps(message['gameState'])
            game = Game.objects.get(pk=message['game_id'])
            save_list = Game_save.objects.filter(game=game, user=request.user)
            if(len(save_list)==0):
                game_save= Game_save(data=json_str, game=game, user=request.user)
                game_save.save()
            else:
                save_list[0].data = json_str
                save_list[0].save


        elif (messageType == "LOAD_REQUEST"):
            # Sent load data and prepare message to send
            game = Game.objects.get(pk=message['game_id'])
            save_list = Game_save.objects.filter(game=game, user=request.user)
            if (len(save_list) == 1):
                loaded_str = save_list[0].data
                gameState=json.loads(loaded_str)
                message = {
                    'messageType': "LOAD",
                    'gameState': gameState
                }
                return_data['message'] = message
        else:
            pass

        return_data['status'] = "success"

        return JsonResponse(return_data)
    else:
        return_data = {'status': "error"}
        return JsonResponse(return_data)