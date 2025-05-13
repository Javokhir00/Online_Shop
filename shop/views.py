from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from shop.forms import OrderForm, ProductForm
from shop.models import Product, Category
from django.contrib.auth.decorators import login_required
from flask import Flask, render_template, request, redirect, url_for
# Create your views here.

def index(request, category_id = None):
    search_query = request.GET.get('q', '')
    categories = Category.objects.all()

    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all() #.order_by('price')

    if search_query:
        products = products.filter(name__icontains = search_query)



    context = {'products': products, 'categories': categories}
    return render(request, 'shop/home.html',  context)

def category_in_detail(request, category_id = None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all()

    context = {'products': products, 'categories': categories,}
    return render(request, 'shop/detail.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        context = {'product': product}
        return render(request, 'shop/detail.html', context)

    except Product.DoesNotExist:
        return HttpResponse('Product Not Found')

def order_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.amount < order.quantity:
                messages.add_message(request, messages.ERROR, 'Product amount isn\'t enough')
            else:
                product.amount -= order.quantity
                product.save()
                order.save()
                messages.add_message(request, messages.SUCCESS, 'Order succesfully created')
                return redirect('product_detail', pk)


    context = {'product': product, 'form': form}
    return render(request, 'shop/order_detail.html', context = context)




@login_required
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form': form}
    return render(request, 'shop/product/create.html', context)




@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return render(request, 'shop/product/delete.html', {'product': product})






app = Flask(__name__)

products = Product.objects.all()

@app.route('/edit/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return render_template('edit.html', product=product)
    else:
        return "Product not found", 404


@app.route('/edit/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        product["name"] = request.form['name']
        product["description"] = request.form['description']
        product["price"] = float(request.form['price'])
        return redirect(url_for('home'))
    else:
        return "Product not found", 404

