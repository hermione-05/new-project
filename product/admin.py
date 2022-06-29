from django.contrib import admin
from numpy import amin
from .models import ColorVariant, Coupon, Item, ProductImage, Reviews, SizeVariant,category

admin.site.register(category)
admin.site.register(Coupon)

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ReviewAdmin(admin.StackedInline):
    model = Reviews

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price']
    inlines = [ProductImageAdmin,ReviewAdmin] 

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color','price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size','price']
    model = SizeVariant

admin.site.register(Item,ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Reviews)
