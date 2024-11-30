from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Game
'''
What views do I want?

A view to show the game board
A view to create a game
A view to show the results of all games and possibly also let you continue an ongoing game
A view to make a player move, which also makes an AI move after the player
'''

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the landing page of tic-tac-toe.")

def board(request: HttpRequest, game_id: int) -> HttpResponse:
    g = Game.objects.get(id=game_id)
    context = {"game": g}
    return render(request, "ttt/board.html", context)
    
    # return HttpResponse(f'''This is a game between {g.player_name}({Game.PLAYER_SYMBOL}) and AI ({Game.AI_SYMBOL}) and this is the board {g}''')
 
def make_move(request: HttpRequest, game_id: int) -> HttpResponse:
    if not request.method == "POST":
        return HttpResponse("Hey, you're only allowed to POST to this endpoint")
    
    row, col = int(request.POST["row"]), int(request.POST["col"])
    g = Game.objects.get(id=game_id)
    g.make_move(row, col, Game.PLAYER_SYMBOL)
    g.make_AI_move()
    g.save()
    
    context = {"game": g}
    return render(request, "ttt/board.html", context)
    
def all_games(request: HttpRequest) -> HttpResponse:
    return HttpResponse("This is supposed to return all active and inactive games")

def active_games(request: HttpRequest) -> HttpResponse:
    return HttpResponse("This is supposed to filter out only active games")