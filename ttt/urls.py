from django.urls import path

from . import views

app_name = 'ttt'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:game_id>", views.board, name="board"),
    path("<int:game_id>/makemove", views.make_move, name="make_move"),
    path("all", views.all_games, name="all_games"),
    path("active", views.active_games, name="active_games")
]