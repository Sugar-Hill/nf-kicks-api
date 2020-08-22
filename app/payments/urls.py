from django.urls import path

from .views import PaymentView


app_name = 'payments'

urlpatterns = [
    path('checkout/', PaymentView.as_view(), name='checkout'),
]
