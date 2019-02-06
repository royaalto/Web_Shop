from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^account/login/', views.login_view),
    url(r'^account/logout/', views.logout_view),
    url(r'^account/register/', views.register_view),
    url(r'^account/email-confirmation/', views.email_confirmation_view),
    url(r'^account/setting/', views.setting_view),
    url(r'^account/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^account/register-success/', views.register_success),
    url(r'^account/social-auth/', views.social_auth),
    url(r'^account/choose-group/', views.choose_group_view),
]
