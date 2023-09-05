from django.urls import path, include
from .views import *

urlpatterns = [
    path('', cart, name="cart"),
    path('add_item/<slug:slug>', add_item, name="add_item"),
    path('add_product/<int:id>', add_product, name="add_product"),
    path('sub_product/<int:id>', sub_product, name="sub_product"),
    path('remove_product/<int:id>', remove_product, name="remove_product"),

    path('checkout/', checkout, name="checkout")
]
