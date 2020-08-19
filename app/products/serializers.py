from rest_framework import serializers
from .models import (
    Product,
    ProductImage,
    ProductVariation,
    Variation,
    Category
)


class CategoryListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:category-detail-view',
        lookup_field='slug'
    )

    class Meta:
        model = Category
        fields = (
            'url',
            'id',
            'title',
        )


class CategoryDetailSerializer(CategoryListSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'products',
        )

    def get_products(self, obj):
        return ProductListSerializer(obj.product_set.all(), many=True, context=self.context).data


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:product-detail-view', lookup_field='slug')

    class Meta:
        model = Product
        fields = (
            'url',
            'id',
            'slug',
            'title',
            'price',
            'image',
        )


class ProductDetailSerializer(ProductListSerializer):
    variations = serializers.SerializerMethodField()
    productImages = serializers.SerializerMethodField()
    categories = CategoryListSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'slug',
            'categories',
            'variations',
            'description',
            'productImages',
        )

    def get_variations(self, obj):
        return VariationSerializer(obj.variation_set.all(), many=True).data

    def get_productImages(self, obj):
        return ProductImageSerializer(
            obj.productimage_set.all(),
            many=True
        ).data


class VariationSerializer(serializers.ModelSerializer):
    productVariation = serializers.SerializerMethodField()

    class Meta:
        model = Variation
        fields = (
            'id',
            'name',
            'productVariation'
        )

    def get_productVariation(self, obj):
        return ProductVariationSerializer(
            obj.productvariation_set.all(),
            many=True
        ).data


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = (
            'id',
            'value',
            'stock'
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id',
            'image',
        )
