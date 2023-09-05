from .models import *
from .views import create_cart


def cart_count(request):

    cart_count = 0
    try:
        cart = Cart.objects.filter(cart_id=create_cart(request))
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
