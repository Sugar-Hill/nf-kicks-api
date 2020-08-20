from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)

from .models import Order

from .serializers import OrderSerializer
# Create your views here.


class OrderListView(ListAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = OrderSerializer
    queryset = Order.objects.all().exclude(order_status='I')
