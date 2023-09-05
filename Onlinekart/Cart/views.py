from django.shortcuts import render, redirect
from django.http import HttpResponse
from Shop.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
# Create your views here.


def create_cart(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(
            cart__cart_id=create_cart(request))
    subtotal = 0

    for item in cart_items:
        subtotal += item.quantity * item.product.price

    shipping = 50
    if(subtotal == 0):
        shipping = 0
    total_amount = subtotal+shipping
    context = {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "shipping": shipping,
        "subtotal": subtotal
    }
    return render(request, "cart.html", context)


def add_item(request, slug):
    product = Product.objects.get(slug=slug)
    try:
        cart = Cart.objects.get(cart_id=create_cart(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=create_cart(request))

    product = Product.objects.get(slug=slug)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user)
        else:
            cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
    except ObjectDoesNotExist:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=request.user)
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, cart=cart)

    cart_item.save()

    return redirect('cart')


def add_product(request, id):

    cart_item = CartItem.objects.get(pk=id)
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


def sub_product(request, id):

    cart_item = CartItem.objects.get(pk=id)
    if (cart_item.quantity > 1):
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_product(request, id):

    cart_item = CartItem.objects.get(pk=id)
    cart_item.delete()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(
            cart__cart_id=create_cart(request))
    subtotal = 0

    for item in cart_items:
        subtotal += item.quantity * item.product.price

    shipping = 50
    if(subtotal == 0):
        shipping = 0
    total_amount = subtotal+shipping
    context = {
        "cart_items": cart_items,
        "total_amount": total_amount,
        "shipping": shipping,
        "subtotal": subtotal
    }
    return render(request, 'checkout.html', context)
