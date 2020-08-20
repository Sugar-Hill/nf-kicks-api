from django.urls import path

from .views import (
    OrderListView,
)


app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    # path('payments/', PaymentListView.as_view(), name='payment-list'),

]
