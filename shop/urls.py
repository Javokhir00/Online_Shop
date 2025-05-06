from django.urls import path
from .views import index, view


urlpatterns = [
    path('', index, name='index'),
    path('product_view/', view, name = 'view'),
]