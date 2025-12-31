# your_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import re
from .models import UserAccount, SellerAccount, Product, SellerProduct, Order, History

class UserAuth:
    @staticmethod
    def validate_password(password):
        if 7 < len(password) < 16:
            if re.search("[^a-zA-Z]", password):
                return True
        return False
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        # Validate
        if not UserAuth.validate_password(password):
            messages.error(request, "Invalid password")
            return redirect('user_register')
        
        if not UserAuth.validate_email(email):
            messages.error(request, "Invalid email")
            return redirect('user_register')
        
        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, "Account already exists!")
            return redirect('user_register')
        
        # Create user
        user = UserAccount(
            full_name=name,
            email=email,
            location=location,
            phone=phone
        )
        user.set_password(password)
        user.save()
        
        messages.success(request, "Account created successfully!")
        return redirect('user_login')
    
    return render(request, 'user_register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = UserAccount.objects.get(email=email)
            if user.check_password(password):
                # Store user ID in session
                request.session['user_id'] = user.user_id
                request.session['user_type'] = 'buyer'
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid password")
        except UserAccount.DoesNotExist:
            messages.error(request, "Account not found")
    
    return render(request, 'user_login.html')

def seller_register(request):
    if request.method == 'POST':
        # Get all form data
        name = request.POST.get('name')
        business_name = request.POST.get('business_name')
        business_type = request.POST.get('business_type')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        location = request.POST.get('location')
        opening_time = request.POST.get('opening_time')
        
        # Validate
        if not UserAuth.validate_password(password):
            messages.error(request, "Invalid password")
            return redirect('seller_register')
        
        if not UserAuth.validate_email(email):
            messages.error(request, "Invalid email")
            return redirect('seller_register')
        
        if SellerAccount.objects.filter(email=email).exists():
            messages.error(request, "Account already exists!")
            return redirect('seller_register')
        
        # Create seller
        seller = SellerAccount(
            full_name=name,
            business_name=business_name,
            business_type=business_type,
            phone=phone,
            email=email,
            location=location,
            opening_time=opening_time,
            rating=0,
            number_of_sales=0
        )
        seller.set_password(password)
        seller.save()
        
        messages.success(request, "Seller account created!")
        return redirect('seller_login')
    
    return render(request, 'seller_register.html')

def seller_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            seller = SellerAccount.objects.get(email=email)
            if seller.check_password(password):
                request.session['seller_id'] = seller.seller_id
                request.session['user_type'] = 'seller'
                messages.success(request, "Login successful!")
                return redirect('seller_dashboard')
            else:
                messages.error(request, "Invalid password")
        except SellerAccount.DoesNotExist:
            messages.error(request, "Account not found")
    
    return render(request, 'seller_login.html')

def home(request):
    if 'user_id' in request.session:
        # Show buyer home page
        products = SellerProduct.objects.select_related('seller', 'product').all()
        return render(request, 'buyer_home.html', {'products': products})
    elif 'seller_id' in request.session:
        # Show seller dashboard
        return redirect('seller_dashboard')
    else:
        return redirect('user_login')

def add_to_cart(request, product_id):
    if 'user_id' not in request.session:
        return redirect('user_login')
    
    # Your cart logic here
    # You can use Django session for cart
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    
    messages.success(request, "Product added to cart!")
    return redirect('home')

def checkout(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    
    user_id = request.session['user_id']
    cart = request.session.get('cart', {})
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        try:
            seller_product = SellerProduct.objects.get(product_id=product_id)
            
            # Create order
            order = Order(
                user_id=user_id,
                product_id=product_id,
                seller_id=seller_product.seller_id,
                price=seller_product.price,
                quantity=quantity,
                total=seller_product.price * quantity
            )
            order.save()
            
            # Add to history
            history = History(
                user_id=user_id,
                product_id=product_id,
                product_qty=quantity,
                price=seller_product.price
            )
            history.save()
            
        except SellerProduct.DoesNotExist:
            continue
    
    # Clear cart
    request.session['cart'] = {}
    messages.success(request, "Order placed successfully!")
    return redirect('order_history')

def logout(request):
    request.session.flush()
    return redirect('home')