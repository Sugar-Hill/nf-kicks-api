from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from products.models import Product, ProductVariation, Variation

# TODO: Make sure this model is correct
from orders.models import OrderItem, Order

from .serializers import OrderSerializer


# Create your views here.
class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        variations = request.data.get('variations', [])
        if slug is None:
            return Response(
                {
                    "message": "Invalid request, please specify a slug!"
                },
                status=HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, slug=slug)

        minimum_variation_count = Variation.objects.filter(
            product=product
        ).count()
        if len(variations) < minimum_variation_count:
            return Response(
                {
                    "message": "Please specify the required variation types"
                },
                status=HTTP_400_BAD_REQUEST
            )

        order_item_qs = OrderItem.objects.filter(
            product=product,
            user=request.user,
            ordered=False
        )
        for v in variations:
            order_item_qs = order_item_qs.filter(
                Q(product_variations__exact=v)
            )

        if order_item_qs.exists():
            order_item = order_item_qs.first()
            order_item.quantity += 1
            order_item.save()
        else:
            order_item = OrderItem.objects.create(
                product=product,
                user=request.user,
                ordered=False
            )
            order_item.product_variations.add(*variations)
            order_item.save()

        order_qs = Order.objects.filter(user=request.user, order_status=1)
        if order_qs.exists():
            order = order_qs[0]
            if not order.order_items.filter(product__id=order_item.id).exists():
                order.order_items.add(order_item)
                return Response(status=HTTP_200_OK)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.order_items.add(order_item)
            return Response(status=HTTP_200_OK)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(
                user=self.request.user, order_status=1)
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")
