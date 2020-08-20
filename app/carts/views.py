from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from .models import CartItem
from products.models import Product, Size
from orders.models import Order

from orders.serializers import OrderSerializer


# Create your views here.
class AddToCartView(APIView):
    permission_classes = (IsAuthenticated,)

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
                    "message": "Please specify the required variations!"
                },
                status=HTTP_400_BAD_REQUEST
            )

        cart_item_qs = CartItem.objects.filter(
            product=product,
            user=request.user,
            ordered=False
        )
        for v in variations:
            cart_item_qs = cart_item_qs.filter(
                Q(product_variations__exact=v)
            )

        if cart_item_qs.exists():
            cart_item = cart_item_qs.first()
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                user=request.user,
                ordered=False
            )
            cart_item.product_variations.add(*variations)
            cart_item.save()

        order_qs = Order.objects.filter(user=request.user, order_status='I')
        if order_qs.exists():
            order = order_qs[0]
            if not order.cart_items.filter(
                product__id=cart_item.id
            ).exists():
                order.cart_items.add(cart_item)
                return Response(status=HTTP_200_OK)

        else:
            order = Order.objects.create(user=request.user)
            order.cart_items.add(cart_item)
            return Response(status=HTTP_200_OK)


class CartView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            order = Order.objects.get(
                user=self.request.user, order_status='I')
            return order
        except ObjectDoesNotExist:
            raise Http404("You do not have an active order")


class CartItemDeleteView(DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = CartItem.objects.all()


class CartItemDecreaseQuantity(APIView):
    permission_classes = (IsAuthenticated,)

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

        cart_item_qs = CartItem.objects.filter(
            product=product,
            user=request.user,
            ordered=False
        )
        for v in variations:
            cart_item_qs = cart_item_qs.filter(
                Q(product_variations__exact=v)
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
