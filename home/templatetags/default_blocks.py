from django import template
from payment.models import Cart
register = template.Library()

@register.inclusion_tag('header.html')
def show_header(user):
    result =  {
            'item_count': Cart.getCartItemCount(user),
            'user':user
            }
    return result


''' 
Edit this inclusion tag for navigation bar or 
only for "all games" part in navgation
'''
@register.inclusion_tag('navigation.html')
def show_navigation():
    return {}