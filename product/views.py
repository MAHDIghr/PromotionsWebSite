from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    products = Product.objects.all()
    bestProducts = Product.objects.all() # a modifier
    return render(request, 'home.html', {'products': products, 'MeilleursProduitsDuMoments' : bestProducts})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product.html', {'product': product})
