from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    Size,
    Category
)


class CategoryInLineAdmin(admin.TabularInline):
    model = Category
    extra = 0
    max_num = 2


class ProductImageInLineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5


class SizeInLineAdmin(admin.TabularInline):
    model = Size
    extra = 0
    max_num = 17


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = [
        'title',
        'price',
        # 'nfc_code',
        'slug',
        'image',
    ]
    inlines = [
        ProductImageInLineAdmin,
        SizeInLineAdmin,
    ]


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    search_fields = ('product__title',)
    list_filter = ('size',)
    list_display = [
        'product',
        'size',
        'stock'
    ]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ('product__title',)
    list_filter = ('product__title',)
    list_display = [
        'product',
        'image',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = [
        'title',
        'slug',
    ]
