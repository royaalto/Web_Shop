from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^game/score-board/$', views.score_board, name='score_board'),
    url(r'^game/score-board/([0-9]+)/$', views.score_board_game, name='score_board'),
    url(r'^game/post/new-score/', views.post_score),
]
