from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^collection/', views.collection_view),
    url(r'^inventory/', views.inventory_view),
]
