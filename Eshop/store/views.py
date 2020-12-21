from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category

# Create your views here.


def index(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.get_all_product_by_category(category_id)
    else:
        products = Product.get_all_product()
    categories = Category.get_all_categories()
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'store.html', data)
