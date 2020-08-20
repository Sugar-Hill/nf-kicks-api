from rest_framework import serializers

from carts.serializers import CartItemSerializer

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'cart_items',
            'ordered_date',
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

# class OrderSerializer(serializers.ModelSerializer):
#     cart_items = serializers.SerializerMethodField()
#     total = serializers.SerializerMethodField()

#     class Meta:
#         model = Order
#         fields = (
#             'id',
#             'cart_items',
#             'total',
#         )

#     def get_cart_items(self, obj):
#         return CartItemSerializer(
#             obj.cart_items.all(),
#             many=True,
#             context=self.context
#         ).data

#     def get_total(self, obj):
#         return obj.get_total()
