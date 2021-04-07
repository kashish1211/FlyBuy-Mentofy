from django.contrib import admin
from .models import Product, CartItem, Cart, CheckoutInfo

admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(CheckoutInfo)