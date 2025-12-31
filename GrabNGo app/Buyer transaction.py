# grabngo/buyer_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, F
from .models import UserAccount, SellerAccount, Product, SellerProduct, Order, History

class BuyerSearchTransactions:
    """Replaces Buyer_Search_Transactions class"""
    @staticmethod
    def search_sellers(request):
        query = request.GET.get('q', '')
        location = request.GET.get('location', '')
        
        sellers = SellerAccount.objects.filter(status='Open')
        
        if query:
            sellers = sellers.filter(
                Q(business_name__icontains=query) |
                Q(full_name__icontains=query) |
                Q(business_type__icontains=query)
            )
        
        if location:
            sellers = sellers.filter(location__icontains=location)
        
        return render(request, 'buyer/search.html', {
            'sellers': sellers,
            'query': query,
            'location': location
        })
    
    @staticmethod
    def search_products(request):
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        
        products = SellerProduct.objects.filter(
            seller__status='Open',
            quantity__gt=0
        ).select_related('product', 'seller')
        
        if query:
            products = products.filter(
                Q(product__product_name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        # Get unique categories for filter
        categories = SellerProduct.objects.values_list(
            'category', flat=True
        ).distinct()
        
        return render(request, 'buyer/products.html', {
            'products': products,
            'query': query,
            'category': category,
            'categories': categories
        })
    
    @staticmethod
    def product_detail(request, product_id, seller_id):
        product = get_object_or_404(SellerProduct, 
            product_id=product_id, 
            seller_id=seller_id
        )
        
        return render(request, 'buyer/product_detail.html', {
            'product': product
        })

class BuyerCartManager:
    """Replaces Buyer_Cart_Manager class"""
    
    @staticmethod
    def add_to_cart(request, product_id, seller_id):
        if 'user_id' not in request.session:
            messages.error(request, "Please login to add items to cart")
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        seller_product = get_object_or_404(SellerProduct, 
            product_id=product_id, 
            seller_id=seller_id
        )
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > seller_product.quantity:
            messages.error(request, "Insufficient stock")
            return redirect('product_detail', product_id=product_id, seller_id=seller_id)
        
        # Check if item already in cart
        existing_order = Order.objects.filter(
            user=user,
            product_id=product_id,
            seller_id=seller_id,
            status='Pending'
        ).first()
        
        if existing_order:
            existing_order.quantity += quantity
            existing_order.total = existing_order.price * existing_order.quantity
            existing_order.save()
            messages.info(request, "Item quantity updated in cart")
        else:
            order = Order(
                user=user,
                product=seller_product.product,
                seller=seller_product.seller,
                price=seller_product.price,
                quantity=quantity,
                total=seller_product.price * quantity,
                status='Pending'
            )
            order.save()
            messages.success(request, "Item added to cart")
        
        return redirect('view_cart')
    
    @staticmethod
    def view_cart(request):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        cart_items = Order.objects.filter(
            user=user,
            status='Pending'
        ).select_related('product', 'seller')
        
        total = sum(item.total for item in cart_items)
        
        return render(request, 'buyer/cart.html', {
            'cart_items': cart_items,
            'total': total
        })
    
    @staticmethod
    def update_cart_item(request, order_id):
        if request.method == 'POST':
            order = get_object_or_404(Order, order_id=order_id, status='Pending')
            quantity = int(request.POST.get('quantity', 1))
            
            seller_product = SellerProduct.objects.get(
                product=order.product,
                seller=order.seller
            )
            
            if quantity > seller_product.quantity:
                messages.error(request, "Insufficient stock")
            else:
                order.quantity = quantity
                order.total = order.price * quantity
                order.save()
                messages.success(request, "Cart updated")
        
        return redirect('view_cart')
    
    @staticmethod
    def remove_from_cart(request, order_id):
        order = get_object_or_404(Order, order_id=order_id, status='Pending')
        order.delete()
        messages.success(request, "Item removed from cart")
        return redirect('view_cart')
    
    @staticmethod
    def empty_cart(request):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        Order.objects.filter(user=user, status='Pending').delete()
        messages.success(request, "Cart emptied")
        return redirect('view_cart')
    
    @staticmethod
    def checkout(request):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        cart_items = Order.objects.filter(user=user, status='Pending')
        
        if not cart_items:
            messages.error(request, "Your cart is empty")
            return redirect('view_cart')
        
        # Check stock availability
        for item in cart_items:
            seller_product = SellerProduct.objects.get(
                product=item.product,
                seller=item.seller
            )
            if item.quantity > seller_product.quantity:
                messages.error(request, f"Insufficient stock for {item.product.product_name}")
                return redirect('view_cart')
        
        # Process each item
        total_amount = 0
        for item in cart_items:
            seller_product = SellerProduct.objects.get(
                product=item.product,
                seller=item.seller
            )
            
            # Update stock
            seller_product.quantity -= item.quantity
            seller_product.save()
            
            # Update product total quantity
            product = seller_product.product
            product.product_qty -= item.quantity
            product.save()
            
            # Create history record
            history = History(
                user=user,
                product=item.product,
                product_qty=item.quantity,
                price=item.price
            )
            history.save()
            
            # Update seller stats
            seller = item.seller
            seller.number_of_sales += 1
            seller.save()
            
            total_amount += item.total
            
            # Mark order as completed
            item.status = 'Completed'
            item.save()
        
        messages.success(request, f"Checkout successful! Total: ${total_amount:.2f}")
        return redirect('order_history')

class BuyerAccountManager:
    """Replaces Buyer_Account_Manager class"""
    @staticmethod
    def update_profile(request):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        
        if request.method == 'POST':
            user.location = request.POST.get('location', user.location)
            user.phone = request.POST.get('phone', user.phone)
            user.save()
            
            messages.success(request, "Profile updated successfully")
            return redirect('buyer_profile')
        
        return render(request, 'buyer/profile.html', {'user': user})
    
    @staticmethod
    def view_history(request):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        user = get_object_or_404(UserAccount, user_id=request.session['user_id'])
        history = History.objects.filter(user=user).order_by('-transaction_date')
        
        return render(request, 'buyer/history.html', {
            'user': user,
            'history': history
        })

class BuyerSubmitReview:
    """Replaces Buyer_Submit_Review class"""
    @staticmethod
    def submit_review(request, seller_id):
        if 'user_id' not in request.session:
            return redirect('user_login')
        
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        
        if request.method == 'POST':
            rating = float(request.POST.get('rating', 0))
            review_text = request.POST.get('review', '')
            
            # Update seller rating
            current_rating = seller.rating
            current_sales = seller.number_of_sales
            
            # Simple average calculation
            new_rating = ((current_rating * current_sales) + rating) / (current_sales + 1)
            
            seller.rating = round(new_rating, 1)
            seller.number_of_sales += 1
            seller.save()
            
            # In a real app, you'd save the review text to a Review model
            messages.success(request, "Thank you for your review!")
            return redirect('seller_detail', seller_id=seller_id)
        
        return render(request, 'buyer/review.html', {'seller': seller})