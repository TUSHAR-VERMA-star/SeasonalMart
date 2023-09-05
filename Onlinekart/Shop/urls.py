from django.urls import path, include
from .views import *

urlpatterns = [
    path('', shop, name="shop"),
    path('search/', search, name="search"),
    path('category/<slug:slug>/', shop, name='products_by_category'),
     path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
]
