from rest_framework import serializers

from products.serializers import (
    ProductListSerializer,
    # ProductVariationSerializer
    SizeSerializer,
)

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_variations = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
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
