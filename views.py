from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('/')


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item = Cart.objects.filter(product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(product=product, quantity=1)

    return redirect('/')


def cart(request):
    items = Cart.objects.all()

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {'items': items, 'total': total})


def increase_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.quantity += 1
    item.save()
    return redirect('/cart')


def decrease_quantity(request, cart_id):
    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('/cart')


def remove_cart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    return redirect('/cart')


def checkout(request):
    cart_items = Cart.objects.select_related('product')

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def place_order(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = Cart.objects.all()

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart_items.delete()

    return render(request, 'order_success.html', {'order': order})