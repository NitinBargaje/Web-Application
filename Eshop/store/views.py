from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Product, Category, Customer, Order
from django.views import View

# Create your views here.


class Index(View):
    def get(self, request):
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

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity == 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        return redirect('homepage')


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        customer = Customer(first_name=postData.get('name'),
                            last_name=postData.get('sirname'),
                            mobile=postData.get('mobile'),
                            email=postData.get('email'),
                            password=postData.get('password'))

        error_message = self.Validate(customer)

        if error_message:
            values = {
                'name': customer.first_name,
                'sirname': customer.last_name,
                'mobile': customer.mobile,
                'email': customer.email
            }
            data = {'error': error_message, 'values': values}
            return render(request, 'signup.html', data)
        else:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')

    def Validate(self, customer):
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


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login = request.POST
        customer = Customer.checkUser(login.get('email'))
        if customer:
            if check_password(login.get('password'), customer.password):
                request.session['customer'] = customer.id
                return redirect('homepage')
            else:
                error_message = 'Incorrect Password!!'
                data = {'error': error_message, 'email': customer.email}
                return render(request, 'login.html', data)
        else:
            return render(request, 'login.html', {'error': 'Email not found'})


class Cart(View):
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_all_product_by_ids(ids)
        return render(request, 'cart.html', {'products': products})


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_all_product_by_ids(
            list(cart.keys()))
        for product in products:
            order = Order(product=product,
                          quantity=cart.get(str(product.id)),
                          price=product.price,
                          customer=Customer(id=customer),
                          phone=phone,
                          address=address,
                          )
            order.placeOrder()
        request.session['cart'] = {}
        return redirect('cart')
