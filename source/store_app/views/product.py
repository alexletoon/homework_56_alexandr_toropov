from django.shortcuts import render, get_object_or_404, redirect
from store_app.models import Product, Choice
from online_store.forms import ProductForm

def index_view(request):
    products = Product.objects.exclude(qty=0).exclude(is_deleted=True).order_by('name')
    context = {'products': products, 'choices': Choice.choices}
    return render(request, 'index.html', context=context)


def display_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product, 'choice': Choice.choices}
    return render(request, 'display_product.html', context=context)


def add_product_view(request):
    product_form = ProductForm()
    if request.method == 'GET':
        context = {'choices': Choice.choices, 'form': product_form}
        return render(request, 'add_product.html', context=context)
    product_form = ProductForm(request.POST)
    if not product_form.is_valid():
        return render(request, 'add_product.html', context={'choices': Choice.choices, 'form': product_form})
    product = Product.objects.create(**product_form.cleaned_data)
    return redirect('index_view')


def edit_product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        product_form = ProductForm(instance=product)
        return render(request, 'edit_product.html', context={'product': product, 'form': product_form})
    product_form = ProductForm(request.POST, instance=product)
    if not product_form.is_valid():
        return render (request, 'edit_product.html', context={'product': product, 'form': product_form})

    product_form.save()
    return redirect('index_view')


def confirm_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'confirm_delete.html', context={'product': product})


def product_deleted_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('index_view')
