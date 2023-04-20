from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from products.forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_edit(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form})

def product_delete(request, pk):
    Product.objects.get(pk=pk).delete()
    return redirect('product_list')

from ..products.models import Product
from ..products.forms import ProductForm


@login_required
def product_management(request):
    if request.user.groups.filter(name='ADMINISTRADOR').exists():
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'product_management.html', context)
    else:
        return redirect('home')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_management')
    template_name = 'product_confirm_delete.html'
    context_object_name = 'product'


@login_required
def product_create(request):
    if request.user.groups.filter(name='ADMINISTRADOR').exists():
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('product_management')
        else:
            form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'product_form.html', context)
    else:
        return redirect('home')


@login_required
def product_update(request, pk):
    if request.user.groups.filter(name='ADMINISTRADOR').exists():
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_management')
        else:
            form = ProductForm(instance=product)
        context = {
            'form': form,
            'product': product
        }
        return render(request, 'product_form.html', context)
    else:
        return redirect('home')
