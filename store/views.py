from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from django.contrib import messages
from .forms import ProductForm


#home page
@login_required(login_url='login')  # 👈 Redirects to login if not logged in
def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})


# Add to Cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    # increment if already added
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')

# Cart Page
@login_required(login_url='login')
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })
        total += item_total

    context = {'items': items, 'total': total}
    return render(request, 'store/cart.html', context)

# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    
    return redirect('cart')

def empty_cart(request):
    request.session['cart'] = {}
    return redirect('cart')

# Increase quantity
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
        request.session['cart'] = cart

    return redirect('cart')


# Decrease quantity
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]  # If 1 → 0, remove item
        request.session['cart'] = cart

    return redirect('cart')
# Signup
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'store/signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'store/signup.html')


# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    return render(request, 'store/login.html')


# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']

        # Create order with dummy total
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            phone=phone,
            total=0
        )

        total = 0
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            item_total = product.price * quantity
            total += item_total

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # Save final total
        order.total = total
        order.save()

        # Clear cart
        request.session['cart'] = {}
        messages.success(request, "✅ Order placed successfully!")
        return redirect('home')

    # GET method: prepare cart summary for display
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        items.append({'product': product, 'quantity': quantity})
        total += product.price * quantity

    context = {'items': items, 'total': total}
    return render(request, 'store/checkout.html', context)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # auto-login after signup
        login(request, user)
        return redirect('home')

    return render(request, 'store/signup.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    orders = OrderItem.objects.filter(product__seller=request.user)
    return render(request, 'store/seller_dashboard.html', {
        'products': products,
        'orders': orders,
    })

@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # agar Product model me seller field hai
            product.save()
            return redirect('my_products')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})

# ✅ Edit Product
@login_required(login_url='login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('my_products')
    return render(request, 'store/product_form.html', {'form': form})

# ✅ Delete Product
@login_required(login_url='login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('my_products')
    return render(request, 'store/confirm_delete.html', {'product': product})

@login_required(login_url='login')
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'store/my_products.html', {'products': products})

