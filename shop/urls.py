from django.urls import path
from .views import index, product_detail, order_detail, create_product, delete_product, category_in_detail

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', index, name='products_by_category'),
    path('category/in_detail/<int:category_id>/', category_in_detail, name='category_in_detail'),
    path('detail/<int:product_id>/',product_detail,name='product_detail'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
    path('product/create/',create_product,name='create_product'),
    path('product/delete/<int:pk>/',delete_product,name='delete_product'),
]