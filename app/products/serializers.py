from rest_framework import serializers

from .models import (
    Product,
    ProductImage,
    Size,
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
            'id',
            'title',
            'url',
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
        # The source of the SSL context override
        return ProductListSerializer(obj.product_set.all(), many=True, context=self.context).data


class ProductListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='products:product-detail-view', lookup_field='slug')

    class Meta:
        model = Product
        fields = (
            'id',
            'slug',
            'title',
            'price',
            'image',
            'url',
        )


class ProductDetailSerializer(ProductListSerializer):
    sizes = serializers.SerializerMethodField()
    productImages = serializers.SerializerMethodField()
    categories = CategoryListSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'price',
            'image',
            'slug',
            'categories',
            'sizes',
            'description',
            'productImages',
        )

    def get_sizes(self, obj):
        return SizeSerializer(obj.size_set.all(), many=True).data

    def get_productImages(self, obj):
        return ProductImageSerializer(
            obj.productimage_set.all(),
            many=True
        ).data


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = (
            'id',
            'size',
            'slug',
            'stock',
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            'id',
            'image',
        )
