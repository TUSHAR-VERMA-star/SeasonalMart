from django.shortcuts import render
from django.http import HttpResponse
from Category.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from django.db.models import Q
# Create your views here.


def shop(request, slug=None):
    categories = None
    products = None
    typeofshop = "OUR SHOP"
    if slug != None:
        categories = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        typeofshop = categories.category_name
        
    else:
        products = Product.objects.all().filter(is_available=True).order_by('price')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
        'typeofshop':typeofshop
    }
    return render(request, "shop.html", context)


def product_detail(request, category_slug, product_slug):
    products = Product.objects.get(category__slug=category_slug, slug=product_slug)
    context={
        'products': products
    }
    return render(request, "product_detail.html", context)

def search(request):

    keyword = request.GET['value']
    products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    product_count = products.count()
    typeofshop = "OUR SHOP"
    context = {
        'products': products,
        'product_count': product_count,
        'typeofshop':typeofshop
    }
    return render(request, 'shop.html', context)