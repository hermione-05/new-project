from .models import Address, Cart, CartItems, Profile
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Address)