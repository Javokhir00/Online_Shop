from django.db.models.functions import Round
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from shop.forms import OrderForm, ProductForm, CommentForm
from shop.models import Product, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.


def filter_by(filter_type, products):

    if filter_type == 'expensive':
        products = products.order_by('-price')

    elif filter_type == 'cheap':
        products = products.order_by('price')


    elif filter_type == 'rating':
        products = products.order_by('-avg_rating')

    return products



def index(request, category_id = None):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    categories = Category.objects.all()


    if category_id:
        products = Product.objects.filter(category = category_id)
    else:
        products = Product.objects.all() #.order_by('price')

    if search_query:
        products = products.filter(name__icontains = search_query)


    products = products.annotate(avg_rating = Round(Avg('comments__rating'), precision = 2))

    products = filter_by(filter_type, products)


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
    return render(request, 'shop/detail.html', context = context)




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


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk)
    else:
        form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, 'shop/detail.html', context)


def comment_create(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', pk)

    context = {'form': form}
    return render(request, 'shop/detail.html', context)



