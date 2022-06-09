from django.contrib import admin
from .models import Cart, CartItem, Address


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)