from django import forms
from shop.models import Order, Product, Comment


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ('created_at', 'updated_at', 'product')



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('created_at', 'updated_at', 'product')