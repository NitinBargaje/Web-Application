from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Category, Customer

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

def Signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        postData = request.POST
        customer = Customer(first_name=postData.get('name'),
        last_name=postData.get('sirname'),
        mobile = postData.get('mobile'),
        email = postData.get('email'),
        password = postData.get('password'))

        error_message = Validate(customer)

        if error_message:
            values = {
                'name':customer.first_name,
                'sirname':customer.last_name,
                'mobile':customer.mobile,
                'email':customer.email
            }
            data = {'error':error_message,'values':values}
            return render(request,'signup.html',data)
        else:
            customer.register()
            return redirect('homepage')

def Validate(customer):
    error_message = None

    if not customer.first_name:
        error_message = 'First name required!!'
    elif len(customer.first_name) < 3:
        error_message = 'Length of name must be 3 character or more'
    elif not customer.last_name:
        error_message = 'Last name required!!'
    elif len(customer.last_name) < 3:
        error_message = 'Length of last name must be 3 character or more'
    elif not customer.email:
        error_message = 'Email required!!'
    elif customer.isExists():
        error_message = 'Email already registered'
    else:
        error_message = None
    return error_message

