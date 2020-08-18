from django.urls import path, include

from .views import (
    ProductListView,
    ProductDetailView,
    CategoryListView,
    CategoryDetailView,
)


app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='products-list-view'),
    path('<slug>', ProductDetailView.as_view(), name='product-detail-view'),
    path('category/', CategoryListView.as_view(), name='category-list-view'),
    path('category/<slug>', CategoryDetailView.as_view(), name='category-detail-view'),

]
