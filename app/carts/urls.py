from django.urls import path, include

from .views import (
    AddToCartView,
    CartView,
    CartItemDeleteView,
    CartItemDecreaseQuantity
)


app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='cart-items'),
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path(
        '<pk>/delete/',
        CartItemDeleteView.as_view(),
        name='cart-item-delete'
    ),
    path(
        'decrease/',
        CartItemDecreaseQuantity.as_view(),
        name='cart-item-decrease-quantity'
    ),
]
