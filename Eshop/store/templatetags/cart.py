from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    for id in cart.keys():
        if int(id) == product.id:
            return True

    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    for id in cart.keys():
        if int(id) == product.id:
            return cart.get(id)

    return False


@register.filter(name='total_price')
def total_price(product, cart):
    return product.price*cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for product in products:
        sum += total_price(product, cart)
    return sum
