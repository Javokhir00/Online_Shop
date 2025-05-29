from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'shop'

from .views import (index,
                    product_detail,
                    order_detail,
                    create_product,
                    delete_product,
                    category_in_detail,
                    edit_product,
                    comment_create,
                    login_page,
                    logout_page)

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', index, name='products_by_category'),
    # path('category/in_detail/<int:category_id>/', category_in_detail, name='category_in_detail'),
    path('detail/<int:product_id>/',product_detail,name='product_detail'),
    path('order/<int:pk>/', order_detail, name='order_detail'),
    path('product/create/',create_product,name='create_product'),
    path('product/delete/<int:pk>/',delete_product,name='delete_product'),
    path('product/edit/<int:pk>/', edit_product, name = 'edit_product'),
    path('comment/create/<int:pk>/', comment_create, name='comment_create'),
    # path('login/', login_page, name = 'login_page'),
    # path('logout/', logout_page, name = 'logout_page'),
    # path('login/', auth_views.LoginView.as_view(next='admin/'), name='login'),

]