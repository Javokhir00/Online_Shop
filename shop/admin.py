from django.contrib import admin
from .models import Product, Category, Order, Comment
from django.contrib.auth.models import User,Group
from adminsortable2.admin import SortableAdminMixin
# from shop.models import SortableBook
# Register your models here.

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','rating','created_at','product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','discount','category']
    search_fields = ['name']
    list_filter = ['price', 'category']


# @admin.register(SortableBook)
# class SortableBookAdmin(SortableAdminMixin, admin.ModelAdmin):
#         list_display = ['name', 'price', 'amount']

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = 'SHOP ONLINE'
admin.site.site_title = 'Online Shop'
admin.site.index_title = "This is online shop"