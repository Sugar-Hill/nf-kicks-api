from rest_framework import serializers

from products.serializers import SizeSerializer

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            'id',
            'size',
            'quantity',
            'final_price'
        )

    def get_size(self, obj):
        return SizeSerializer(obj.size, context=self.context).data

    def get_final_price(self, obj):
        return obj.get_final_price()
