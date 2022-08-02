from django.contrib import admin

from store.models import Product, ShoppingCartItem, ShoppingCart

admin.site.register(Product)
admin.site.register(ShoppingCartItem)
admin.site.register(ShoppingCart)

