from django.contrib import admin
from .models import Product, Category
from django.contrib.auth.models import User,Group

# Register your models here.

admin.site.register(Product)

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','discount','category']
    search_fields = ['name']
    list_filter = ['price']



admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.site_header = 'SHOP ONLINE'
admin.site.site_title = 'Online Shop'
admin.site.index_title = "this is online shop"