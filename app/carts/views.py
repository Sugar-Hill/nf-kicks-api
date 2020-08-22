from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import CartItem
from products.models import Size
from orders.models import Order

from orders.serializers import OrderSerializer


# Create your views here.
class AddToCartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response(
                {
                    "message": "Invalid request, please specify a slug!"
                },
                status=HTTP_400_BAD_REQUEST
            )

        size = get_object_or_404(Size, slug=slug)

        if size.stock > 1:
            cart_item_qs = CartItem.objects.filter(
                size=size,
                user=request.user,
                ordered=False
            )

            if cart_item_qs.exists():
                cart_item = cart_item_qs.first()
                cart_item.quantity += 1
                cart_item.save()
                return Response(status=HTTP_200_OK)
            else:
                cart_item = CartItem.objects.create(
                    size=size,
                    user=request.user,
                    ordered=False
                )
                cart_item.save()

            order_qs = Order.objects.filter(
                user=request.user, order_status='In Cart')
            if order_qs.exists():
                order = order_qs[0]
                if not order.cart_items.filter(size__id=cart_item.id).exists():
                    order.cart_items.add(cart_item)
                    return Response(status=HTTP_200_OK)

            else:
                order = Order.objects.create(user=request.user)
                order.cart_items.add(cart_item)
                return Response(status=HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "This item's size is out of stock!"
                },
                status=HTTP_400_BAD_REQUEST
            )


class CartView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(
                user=self.request.user, order_status='In Cart')
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")


class CartItemDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CartItem.objects.all()


class ReduceCartItem(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        slug = request.data.get('slug', None)
        if slug is None:
            return Response(
                {
                    "message": "Invalid request, please specify a slug!"
                },
                status=HTTP_400_BAD_REQUEST
            )

        size = get_object_or_404(Size, slug=slug)

        cart_item_qs = CartItem.objects.filter(
            size=size,
            user=request.user,
            ordered=False
        )

        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # TODO: Might be the source of a problem
                cart_item.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response(
                {
                    "message": "This item was not in your cart"
                },
                status=HTTP_400_BAD_REQUEST
            )
