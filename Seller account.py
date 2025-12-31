# grabngo/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import datetime

class UserAccount(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.full_name

class SellerAccount(models.Model):
    seller_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    location = models.CharField(max_length=200)
    opening_time = models.TimeField()
    rating = models.FloatField(default=0.0)  # Changed from IntegerField
    number_of_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')
    profile_pic = models.CharField(max_length=255, blank=True, null=True)  # Added for profile pics
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.business_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_qty = models.IntegerField(default=0)
    
    def __str__(self):
        return self.product_name

class SellerProduct(models.Model):
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    product_image_path = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        unique_together = ['seller', 'product']
    
    def __str__(self):
        return f"{self.product.product_name} - {self.seller.business_name}"

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')  # Changed from 'Active'
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.product.product_name}"

class History(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction #{self.transaction_id} - {self.user.full_name}"