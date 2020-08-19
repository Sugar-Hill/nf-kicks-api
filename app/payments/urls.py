from django.urls import path, include

from .views import (
    PaymentView,
    PaymentListView
)


app_name = 'payments'

urlpatterns = [
    path('checkout/', PaymentView.as_view(), name='checkout'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),

]
