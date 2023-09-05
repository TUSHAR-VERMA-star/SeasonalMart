from django.shortcuts import render
from django.http import HttpResponse
from Category.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from Shop.models import *



def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('price')
    bestproducts = Product.objects.all().filter(is_available=True).order_by('id')[:3]
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()


    context = {
        'products': paged_products,
        'product_count': product_count,
        'bestproducts':bestproducts,
    }
    return render(request, "home.html", context)