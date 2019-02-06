from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from payment.models import Cart, Item
from game.models import Game
from django.contrib import messages
from django.http import JsonResponse
from hashlib import md5

# Create your views here.

# Secret key used for payment SID
PAYMENT_SID = 'melonPayment503'
SECRET_KEY = "5bb977d6a1ee9c74f6e1685994714445"

def decimalToPriceTag(decimal):
    return str(decimal)+'€'


def payment_view(request):

    if request.user.is_authenticated:
        if request.user.groups.get(name='Player'):
            # Find active cart
            current_user = request.user
            cart = Cart.getActiveCart(user=current_user)

            context = {}
            context['total_price'] = decimalToPriceTag(cart.total_price)
            context['item_count']  = cart.total_qty
            context['items'] = cart.item.all()

            return render(request, "payment/cart.html", context)
    return render(request, "403.html")



def order_view(request):
    if request.user.is_authenticated:
        if request.user.groups.get(name='Player'):
            context = {'item_count':Cart.getActiveCart(request.user).total_qty}

            # Find active cart
            cart = Cart.getActiveCart(user=request.user)

            if(cart.total_price == 0):
                context['empty_cart']=True
            if not cart.validateItemPrices():
                messages.add_message(request, messages.ERROR, 'Some product prices have changed. Not able to buy it anymore. Reselect product in order to buy it.')
                return redirect('/payment/cart')

            context['total_price'] = decimalToPriceTag(cart.total_price)
            context['item_count'] = cart.total_qty
            context['items'] = cart.item.all()

            context['pid'] = "order"+str(cart.id)
            context['sid'] = PAYMENT_SID
            context['amount'] = cart.total_price

            checksumstr = "pid={}&sid={}&amount={}&token={}".format(context['pid'], context['sid'], context['amount'], SECRET_KEY)

            m = md5(checksumstr.encode("ascii"))
            checksum = m.hexdigest()

            context['checksum'] = checksum
            context['page_url'] = request.META['HTTP_HOST']

            return render(request, "payment/order.html", context)
    return render(request, "403.html")


def success_view(request):
    context = {'success':True}
    if request.method == 'GET':
        # Check if GET request have all data
        get = request.GET
        if (
                not get.__contains__('pid') or
                not get.__contains__('ref') or
                not get.__contains__('result') or
                not get.__contains__('checksum')
        ):
            context['success'] = False
        else:
            pid = get['pid']
            ref = get['ref']
            result = get['result']
            checksum = get['checksum']

            checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, SECRET_KEY)
            m = md5(checksumstr.encode("ascii"))
            confirm_checksum = m.hexdigest()

            # Verity checksum
            if(confirm_checksum!=checksum):
                context['success'] = False
            else:
                # Checksum correct
                cart = Cart.getActiveCart(request.user)
                if(pid == 'order'+str(cart.id)):
                    cart.buyCart()
    context['item_count'] = Cart.getActiveCart(request.user).total_qty
    return render(request, "payment/success.html", context)



def error_view(request):
    context = {'item_count': Cart.getCartItemCount(request.user)}
    context['success'] =request.META['HTTP_HOST']+'/payment/error'
    return render(request, "payment/error.html", context)



def cancel_view(request):
    # This view not used anymore
    context = {'item_count': Cart.getCartItemCount(request.user)}
    context['success']=request.build_absolute_uri()
    context['success'] =request.META['HTTP_HOST']+'/payment/cancel'
    return render(request, "payment/cancel.html", context)


def delete_item(request):
    # Delete item from the cart
    if request.method == "POST" and request.is_ajax():
        item_id = request.POST['item_id']
        cart = Cart.getActiveCart(user=request.user)
        item = Item.objects.get(pk=item_id)
        item.delete()
        cart.save()
        data = {'status': "success"}
        messages.add_message(request, messages.INFO, 'Item deleted.')

        return JsonResponse(data)
    else:
        data = {'status': "error"}
        return JsonResponse(data)

def add_item(request):
    if request.method == "POST" and request.is_ajax():

        game_id = request.POST['game_id']
        cart = Cart.getActiveCart(user=request.user)

        # if game already in cart, increase qty
        for i in cart.item.all():
            if i.game.id == int(game_id):
                i.qty += 1
                i.save()
                cart.save()

                messages.add_message(request, messages.INFO, 'Game quantity increased.')
                data = {'status': "success"}
                return JsonResponse(data)

        # Add game to the cart
        game = Game.objects.get(pk=game_id)
        if(game):
            item = Item(game=game)
            item.save()
            cart.item.add(item)
            cart.save()
            result = "success"
            messages.add_message(request, messages.INFO, 'Game added to the cart.')
        else:
            result = 'failed'
            messages.add_message(request, messages.ERROR, 'Could not add game to the cart.')

        data = {'status': result}
        return JsonResponse(data)
    else:
        data = {'status': "error"}
        return JsonResponse(data)


