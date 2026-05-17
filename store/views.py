from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Product, Order, OrderItem, Wishlist

import razorpay
from django.conf import settings


# 🏠 Home Page
def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'store/home.html', {
        'products': products
    })


# ➕ Add to Cart
def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    return redirect('home')


# 🛒 Cart Page
def cart_view(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for key, value in cart.items():

        product = Product.objects.get(id=key)

        product.quantity = value
        product.total_price = product.price * value

        total += product.total_price

        products.append(product)

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


# ❌ Remove Item
def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


# ➕ Increase Quantity
def increase_quantity(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart

    return redirect('cart')


# ➖ Decrease Quantity
def decrease_quantity(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:

        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')


# 💳 Checkout
@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for key, value in cart.items():

        product = Product.objects.get(id=key)

        product.quantity = value
        product.total_price = product.price * value

        total += product.total_price

        products.append(product)

    # 🔥 Razorpay Client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": int(total * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, 'store/checkout.html', {
        'products': products,
        'total': total,
        'payment': payment,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })


# 💵 COD SUCCESS
@login_required
def cod_success(request):

    name = request.GET.get('name')
    address = request.GET.get('address')

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for key, value in cart.items():

        product = Product.objects.get(id=key)

        product.quantity = value
        product.total_price = product.price * value

        total += product.total_price

        products.append(product)

    # 🔥 CREATE ORDER
    order = Order.objects.create(
        user=request.user,
        name=name,
        address=address,
        total_amount=total,
        status='Pending'
    )

    # 🔥 SAVE ORDER ITEMS
    for product in products:

        OrderItem.objects.create(
            order=order,
            product_name=product.name,
            price=product.price,
            quantity=product.quantity
        )

    # 🧹 CLEAR CART
    request.session['cart'] = {}

    return render(request, 'store/success.html')


# ✅ Payment Success
@login_required
def payment_success(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for key, value in cart.items():

        product = Product.objects.get(id=key)

        product.quantity = value
        product.total_price = product.price * value

        total += product.total_price

        products.append(product)

    # 🔥 CREATE ORDER
    order = Order.objects.create(
        user=request.user,
        name=request.user.username,
        address="Online Payment",
        total_amount=total,
        status='Paid'
    )

    # 🔥 SAVE ITEMS
    for product in products:

        OrderItem.objects.create(
            order=order,
            product_name=product.name,
            price=product.price,
            quantity=product.quantity
        )

    # 🧹 CLEAR CART
    request.session['cart'] = {}

    return render(request, 'store/success.html')


# ❌ Payment Failed
def payment_failed(request):

    return render(request, 'store/failed.html')


# 📦 My Orders
@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'store/orders.html', {
        'orders': orders
    })


# 🔍 Order Detail
@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    items = OrderItem.objects.filter(order=order)

    return render(request, 'store/order_detail.html', {
        'order': order,
        'items': items
    })


# ❌ Cancel Order
@login_required
def cancel_order(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    if order.status == "Pending":

        order.status = "Cancelled"
        order.save()

    return redirect('my_orders')


# 📝 Signup
def signup(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'store/signup.html')


# 👤 Profile
@login_required
def profile(request):

    orders = Order.objects.filter(user=request.user)

    total_orders = orders.count()

    total_spent = 0

    for order in orders:
        total_spent += order.total_amount

    return render(request, 'store/profile.html', {
        'total_orders': total_orders,
        'total_spent': total_spent
    })


# ❤️ Add To Wishlist
@login_required
def add_to_wishlist(request, id):

    product = Product.objects.get(id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('home')


# ❤️ Wishlist Page
@login_required
def wishlist(request):

    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'store/wishlist.html', {
        'items': items
    })


# 👟 Product Detail
def product_detail(request, id):

    product = Product.objects.get(id=id)

    return render(request, 'store/product_detail.html', {
        'product': product
    })