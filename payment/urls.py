from django.conf.urls import url

from payment import views

urlpatterns = [

    url(r'^payment/delete/item/$', views.delete_item, name='validate_username'),
    url(r'^payment/add/item/$', views.add_item, name='validate_username'),
    url(r'^payment/cart/$', views.payment_view),
    url(r'^payment/order/$', views.order_view),
    url(r'^payment/success/', views.success_view),
    url(r'^payment/cancel/', views.payment_view),
    url(r'^payment/error/', views.error_view),
]
