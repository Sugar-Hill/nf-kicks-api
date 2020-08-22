from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .models import Order

from .serializers import PaymentOrderSerializer, PaymentOrderDetailSerializer


class OrderListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentOrderSerializer
    queryset = Order.objects.all().exclude(order_status='In Cart')


class OrderDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentOrderDetailSerializer
    queryset = Order.objects.all().exclude(order_status='In Cart')
