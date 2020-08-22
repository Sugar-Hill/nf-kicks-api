from django.urls import path, include

from .views import (
    AddToCartView,
    CartView,
    CartItemDeleteView,
    ReduceCartItem
)


app_name = 'carts'

urlpatterns = [
    path('', CartView.as_view(), name='cart-items'),
    path('add/', AddToCartView.as_view(), name='add-to-item-cart'),
    path(
        '<pk>/delete/',
        CartItemDeleteView.as_view(),
        name='cart-item-delete'
    ),
    path(
        'reduce/',
        ReduceCartItem.as_view(),
        name='reduce-cart-item-quantity'
    ),
]
