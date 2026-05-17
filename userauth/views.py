from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def signup(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 🔥 Password Match Check
        if password != confirm_password:
            return render(request, 'store/signup.html', {
                'error': 'Passwords do not match'
            })

        # 🔥 Username Exists Check
        if User.objects.filter(username=username).exists():
            return render(request, 'store/signup.html', {
                'error': 'Username already exists'
            })

        # ✅ Create User
        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)

        return redirect('home')

    return render(request, 'store/signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'userauth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'userauth/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart
    return redirect('home')


from django.http import HttpResponse

def view_cart(request):
    return HttpResponse(request.session.get('cart', {}))