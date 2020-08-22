from django.contrib import admin

from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_filter = ('ordered',)
    search_fields = ('user__username', 'size__size', 'size__product__title',)
    list_display = [
        'user',
        'ordered',
        'size',
        'quantity'
    ]
