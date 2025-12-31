# grabngo/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from grabngo.models import UserAccount, SellerAccount, Product, SellerProduct, Order, History
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populates the database with sample Cameroonian data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Populating database with sample data...")
        
        # Clear existing data
        UserAccount.objects.all().delete()
        SellerAccount.objects.all().delete()
        Product.objects.all().delete()
        
        # Create buyers
        buyers_data = [
            ("Ngo Batoum Marie", "marie.bat@camnet.cm", "Akwa, Douala", "699123456"),
            ("Tanyi Kevin Ashu", "kevin.ashu@gmail.com", "Molyko, Buea", "677889900"),
            # ... add more from your list
        ]
        
        for name, email, location, phone in buyers_data:
            user = UserAccount(
                full_name=name,
                email=email,
                location=location,
                phone=phone
            )
            user.set_password("password123")
            user.save()
        
        # Create sellers
        sellers_data = [
            ("Fosso Kamga", "Fosso Wholesale", "Food & Beverage", "677978500", 
             "fosso@gmail.com", "Marché Central, Yaoundé", "08:00:00"),
            # ... add more from your list
        ]
        
        for name, business_name, business_type, phone, email, location, opening_time in sellers_data:
            seller = SellerAccount(
                full_name=name,
                business_name=business_name,
                business_type=business_type,
                phone=phone,
                email=email,
                location=location,
                opening_time=opening_time,
                rating=4.5,
                number_of_sales=120
            )
            seller.set_password("password123")
            seller.save()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database'))