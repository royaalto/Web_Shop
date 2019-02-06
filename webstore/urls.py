"""webstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from account import views as account
from game import views as game
from payment import views as payment
from home import views as home
from collection import views as collection
from game_data import views as game_data
from home.views import home_view
from home.views import *

#from django.conf.urls import handler404


urlpatterns = [

    url(r'', include('account.urls')),
    url(r'', include('game.urls')),
    url(r'', include('payment.urls')),
    url(r'', include('home.urls'), name='home'),
    url(r'', include('collection.urls')),
    url(r'', include('game_data.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),#face
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = error_404
