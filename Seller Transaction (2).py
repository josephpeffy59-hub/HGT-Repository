# grabngo/seller_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, F, Count
from datetime import datetime, timedelta
from .models import SellerAccount, Product, SellerProduct, Order, History

class SellerView:
    """Replaces Seller_View class"""
    @staticmethod
    def view_store(request, seller_id):
        if 'seller_id' not in request.session or request.session['seller_id'] != seller_id:
            return redirect('seller_login')
        
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        products = SellerProduct.objects.filter(seller=seller).select_related('product')
        
        return render(request, 'seller/store.html', {
            'seller': seller,
            'products': products
        })
    
    @staticmethod
    def view_orders(request, seller_id):
        if 'seller_id' not in request.session or request.session['seller_id'] != seller_id:
            return redirect('seller_login')
        
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        orders = Order.objects.filter(seller=seller).select_related('product', 'user')
        
        return render(request, 'seller/orders.html', {
            'seller': seller,
            'orders': orders
        })

class SellerStoreManager:
    """Replaces Seller_Store_Manager class"""
    @staticmethod
    def add_to_store(request, seller_id):
        if request.method == 'POST':
            seller = get_object_or_404(SellerAccount, seller_id=seller_id)
            
            product_name = request.POST.get('product_name')
            description = request.POST.get('description')
            category = request.POST.get('category')
            price = request.POST.get('price')
            quantity = request.POST.get('quantity')
            image_path = request.POST.get('image_path', '')
            
            # Check if product exists
            product, created = Product.objects.get_or_create(
                product_name=product_name,
                defaults={'product_qty': 0}
            )
            
            if created:
                product.product_qty = int(quantity)
                product.save()
            else:
                product.product_qty += int(quantity)
                product.save()
            
            # Create or update SellerProduct
            seller_product, created = SellerProduct.objects.get_or_create(
                seller=seller,
                product=product,
                defaults={
                    'description': description,
                    'category': category,
                    'price': price,
                    'quantity': quantity,
                    'product_image_path': image_path
                }
            )
            
            if not created:
                seller_product.quantity += int(quantity)
                seller_product.save()
                messages.info(request, "Product quantity updated")
            else:
                messages.success(request, "Product added to store")
            
            return redirect('seller_store', seller_id=seller_id)
    
    @staticmethod
    def update_store_status(request, seller_id, status):
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        seller.status = status
        seller.save()
        
        status_msg = "opened" if status == "Open" else "closed"
        messages.success(request, f"Store has been {status_msg}")
        return redirect('seller_dashboard')
    
    @staticmethod
    def update_product_quantity(request, seller_id, product_id):
        if request.method == 'POST':
            seller = get_object_or_404(SellerAccount, seller_id=seller_id)
            seller_product = get_object_or_404(SellerProduct, seller=seller, product_id=product_id)
            product = seller_product.product
            
            new_quantity = int(request.POST.get('quantity'))
            old_quantity = seller_product.quantity
            
            # Update SellerProduct quantity
            seller_product.quantity = new_quantity
            seller_product.save()
            
            # Update Product total quantity
            quantity_diff = new_quantity - old_quantity
            product.product_qty += quantity_diff
            product.save()
            
            messages.success(request, "Product quantity updated")
            return redirect('seller_store', seller_id=seller_id)
    
    @staticmethod
    def update_product_price(request, seller_id, product_id):
        if request.method == 'POST':
            seller = get_object_or_404(SellerAccount, seller_id=seller_id)
            seller_product = get_object_or_404(SellerProduct, seller=seller, product_id=product_id)
            
            new_price = request.POST.get('price')
            seller_product.price = new_price
            seller_product.save()
            
            messages.success(request, "Product price updated")
            return redirect('seller_store', seller_id=seller_id)
    
    @staticmethod
    def delete_product(request, seller_id, product_id):
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        seller_product = get_object_or_404(SellerProduct, seller=seller, product_id=product_id)
        product = seller_product.product
        
        # Update Product total quantity
        product.product_qty -= seller_product.quantity
        product.save()
        
        # Delete SellerProduct
        seller_product.delete()
        
        messages.success(request, "Product deleted from store")
        return redirect('seller_store', seller_id=seller_id)
    
    @staticmethod
    def calculate_income(request, seller_id, period):
        """Calculate income for daily, weekly, monthly, yearly"""
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        
        # Determine date range based on period
        now = datetime.now()
        if period == 'daily':
            start_date = now - timedelta(days=1)
        elif period == 'weekly':
            start_date = now - timedelta(days=7)
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
        elif period == 'yearly':
            start_date = now - timedelta(days=365)
        else:
            start_date = now - timedelta(days=365)  # Default to yearly
        
        # Get orders within date range
        orders = Order.objects.filter(
            seller=seller,
            created_at__gte=start_date,
            status='Completed'  # Only completed orders
        )
        
        total_income = orders.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0
        
        period_names = {
            'daily': 'Daily',
            'weekly': 'Weekly', 
            'monthly': 'Monthly',
            'yearly': 'Yearly'
        }
        
        return JsonResponse({
            'period': period_names.get(period, 'Yearly'),
            'income': float(total_income),
            'order_count': orders.count()
        })
    
    @staticmethod
    def seller_statistics(request, seller_id):
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        
        # Get completed orders
        orders = Order.objects.filter(seller=seller, status='Completed')
        
        # Product statistics
        product_stats = orders.values(
            'product__product_name'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_revenue=Sum(F('price') * F('quantity'))
        ).order_by('-total_quantity')
        
        if product_stats:
            max_product = product_stats.first()
            min_product = product_stats.last()
        else:
            max_product = min_product = None
        
        return render(request, 'seller/statistics.html', {
            'seller': seller,
            'product_stats': product_stats,
            'max_product': max_product,
            'min_product': min_product,
            'total_orders': orders.count(),
            'total_revenue': orders.aggregate(
                total=Sum(F('price') * F('quantity'))
            )['total'] or 0
        })

class SellerAccountManager:
    """Replaces Seller_Account_Manager class"""
    @staticmethod
    def update_profile(request, seller_id):
        if request.method == 'POST':
            seller = get_object_or_404(SellerAccount, seller_id=seller_id)
            
            # Update fields
            seller.location = request.POST.get('location', seller.location)
            seller.business_name = request.POST.get('business_name', seller.business_name)
            seller.opening_time = request.POST.get('opening_time', seller.opening_time)
            
            # Handle profile picture
            if 'profile_pic' in request.FILES:
                # In production, you'd save to media files
                seller.profile_pic = f"profile_pics/{request.FILES['profile_pic'].name}"
            
            seller.save()
            messages.success(request, "Profile updated successfully")
            return redirect('seller_profile', seller_id=seller_id)
    
    @staticmethod
    def delete_account(request, seller_id):
        if request.method == 'POST':
            seller = get_object_or_404(SellerAccount, seller_id=seller_id)
            
            # Delete all seller products first
            SellerProduct.objects.filter(seller=seller).delete()
            
            # Delete seller account
            seller.delete()
            
            # Clear session
            request.session.flush()
            
            messages.success(request, "Account deleted successfully")
            return redirect('home')
    
    @staticmethod
    def view_history(request, seller_id):
        seller = get_object_or_404(SellerAccount, seller_id=seller_id)
        
        # Get orders for this seller
        orders = Order.objects.filter(seller=seller).order_by('-created_at')
        
        return render(request, 'seller/history.html', {
            'seller': seller,
            'orders': orders
        })