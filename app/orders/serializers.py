from rest_framework import serializers

from carts.serializers import CartItemSerializer
from payments.serializers import PaymentSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'cart_items',
            'start_date',
            'total',
        )

    def get_cart_items(self, obj):
        return CartItemSerializer(
            obj.cart_items.all(),
            many=True,
            context=self.context
        ).data

    def get_total(self, obj):
        return obj.get_total()


class PaymentOrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='orders:order-detail-view'
    )
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'url',
            'payment',
            'order_status',
        )

    def get_payment(self, obj):
        return PaymentSerializer(obj.payment).data


class PaymentOrderDetailSerializer(PaymentOrderSerializer):
    cart_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'cart_items',
            'payment',
            'order_status',
            'total',
        )

    def get_cart_items(self, obj):
        return CartItemSerializer(
            obj.cart_items.all(),
            many=True,
            context=self.context
        ).data

    def get_total(self, obj):
        return obj.get_total()

    def get_payment(self, obj):
        return PaymentSerializer(obj.payment).data
