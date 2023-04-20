from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy

from .models import Product
from .forms import ProductForm


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

