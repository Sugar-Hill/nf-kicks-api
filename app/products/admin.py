from django.contrib import admin

from .models import (
    Product,
    ProductImage,
    ProductVariation,
    Variation,
    Category
)


class CategoryInLineAdmin(admin.TabularInline):
    model = Category
    extra = 0
    max_num = 5


class ProductImageInLineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5


class VariationInLineAdmin(admin.TabularInline):
    model = Variation
    extra = 0
    max_num = 2


class ProductVariationInLineAdmin(admin.TabularInline):
    model = ProductVariation
    extra = 0
    max_num = 12


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'price',
        'slug',
        'image',
    ]
    inlines = [
        ProductImageInLineAdmin,
        VariationInLineAdmin,
    ]


class VariationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'product',
    ]
    inlines = [
        ProductVariationInLineAdmin,
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductVariation)
