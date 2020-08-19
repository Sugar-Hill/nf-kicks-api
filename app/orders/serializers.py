from rest_framework import serializers

from .models import Order, OrderItem

from products.serializers import (
    ProductListSerializer,
    ProductVariationSerializer
)


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_variations = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'product_variations',
            'quantity',
            'final_price'
        )

    def get_product(self, obj):
        return ProductListSerializer(obj.product, context=self.context).data

    def get_product_variations(self, obj):
        return ProductVariationSerializer(
            obj.product_variations.all(),
            many=True
        ).data

    def get_final_price(self, obj):
        return obj.get_final_price()


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'order_items',
            'total',
        )

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.order_items.all(), many=True, context=self.context).data

    def get_total(self, obj):
        return obj.get_total()
