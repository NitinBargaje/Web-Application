from django.contrib import admin
from django.urls import path
from .views import Index, Signup, Login, Cart, CheckOut

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('cart', Cart.as_view(), name = 'cart'),
    path('check-out', CheckOut.as_view(), name = 'checkout')
]
