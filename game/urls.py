from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^game/edit/(\d+)', views.edit_view),
    url(r'^game/search/', views.search, name='search'),
    url(r'^game/play/([0-9]+)/$', views.play_view,name='play'),
    url(r'^game/description/([0-9]+)/$', views.description),
    url(r'^game/statistic/([0-9]+)/$', views.statistic_view),
    url(r'^game/edit/new/$', views.new_edit_view),
    url(r'^search/category/(?P<pk>[0-9]+)/$', views.category, name='category'),
]
