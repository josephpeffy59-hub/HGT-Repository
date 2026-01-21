# ===============================
# STANDARD IMPORTS
# ===============================
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from datetime import datetime
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    DictProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen,SlideTransition
from kivy.uix.recycleview import RecycleView
from datetime import datetime


# ===============================
# BACKEND IMPORTS (UNCHANGED)
# ===============================
import sqlite3
import os

from BackEnd.Buyer_Login import Buyer_Login
from BackEnd.Seller_Login import Seller_Login
from BackEnd.Buyer_Transaction import *
from BackEnd.Seller_Transaction import *
from BackEnd.Delivery_agent_login import *
from BackEnd.Delivery_agent_transactions import *

# ===============================
# DATABASE CONNECTION
# ===============================
con = Get_Database_connection()

Window.clearcolor = (1, 1, 1, 1)
Window.softinput_mode = 'below_target'


# ===============================
# FIRST / LANDING PAGE
# ===============================
class First_Page(Screen):
    pass


# ===============================
# BUYER LOGIN
# ===============================
class Buyer_Login_Page(Screen):
    login_text = StringProperty("")
    answer_to_password_forgotten = StringProperty("")
    print("********************")

    def Buyer_Loginto_app(self):
        self.Logs = Buyer_Login(con)

        buyer_name = self.ids.buyer_login_name.text.strip()
        buyer_email = self.ids.buyer_login_email.text.strip()
        buyer_password = self.ids.buyer_login_password.text.strip()

        if not buyer_name:
            self.login_text = "Please Enter your UserName"
            return
        if not buyer_email:
            self.login_text = "Please Enter your Email"
            return
        if not buyer_password:
            self.login_text = "Please Enter your Password"
            return

        result = self.Logs.login(buyer_name, buyer_email, buyer_password)


        if result == 1:
            info = self.Logs.Get_buyer_info(buyer_name)
            print(info)
            App.get_running_app().buyer_name=info[0][1]
            App.get_running_app().buyer_id = info[0][0]
            App.get_running_app().buyer_location = info[0][3]
            App.get_running_app().buyer_phone = info[0][4]
            App.get_running_app().buyer_password = info[0][5]
            App.get_running_app().buyer_email = info[0][2]

            self.manager.current = "buyerdashboard"
        else:
            self.login_text = str(result)

    def fogot_password(self):
        self.answer_to_password_forgotten = "To get your password, contact our team"



# ===============================
# SELLER LOGIN
# ===============================
class Seller_Login_Page(Screen):
    login_text = StringProperty("")
    answer_to_password_forgotten = StringProperty("")

    def Seller_Loginto_app(self):
        self.Logs = Seller_Login(con)
        print("*********************************")

        seller_name = self.ids.seller_login_name.text.strip()
        seller_email = self.ids.seller_login_email.text.strip()
        seller_password = self.ids.seller_login_password.text.strip()

        if not seller_name:
            self.login_text = "Please Enter your UserName"
            return
        if not seller_email:
            self.login_text = "Please Enter your Email"
            return
        if not seller_password:
            self.login_text = "Please Enter your Password"
            return

        result = self.Logs.login(seller_name, seller_email, seller_password)

        if result == 1:
            self.login_text = "Login in............"

            info = self.Logs.Get_seller_info(seller_name)
            print("************^^^&&&&&&&&&&^***********")
            print(info)
            App.get_running_app().seller_name=info[0][1]
            App.get_running_app().seller_email=info[0][5]
            App.get_running_app().seller_password=info[0][6]
            App.get_running_app().seller_location=info[0][7]
            App.get_running_app().seller_phone=info[0][4]
            App.get_running_app().seller_id = info[0][0]

            App.get_running_app().buisness_name = info[0][2]
            App.get_running_app().buisness_type = info[0][3]
            App.get_running_app().seller_opening_time = info[0][8]
            App.get_running_app().seller_rating = int(info[0][9])
            App.get_running_app().seller_number_of_sales=info[0][10]


            self.manager.current = "seller_manager_page"
        else:
            self.login_text = str(result)

    def forgot_password(self):
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        self.answer_to_password_forgotten = "To get your password, contact our team"


# ===============================
# CREATE BUYER ACCOUNT
# ===============================
class Create_Buyer_Account_Page(Screen):
    login_text=StringProperty("")
    def get_formatted_date(self):
    	# This returns the current date in the exact DD-MM-YY format
        return datetime.now().strftime("%d-%m-%y")

    def buyer_create_account(self):
        self.date=self.get_formatted_date()
        self.creater=Buyer_Login(con)
        buyer_name= (self.ids.buyer_create_account_name.text).strip()
        buyer_email=(self.ids.buyer_create_account_email.text).strip()
        buyer_password=(self.ids.buyer_create_account_password.text).strip()
        buyer_location=((self.ids.buyer_create_account_location.text).strip()).lower()
        buyer_phone=(self.ids.buyer_create_account_phone.text).strip()
        if buyer_name=="":
            self.login_text="Please Enter your UserName"
            return 0
        if buyer_email=="":
            self.login_text="Please Enter your Email"
            return 0
        if buyer_password=="":
            self.login_text="Please Enter your Password"
            return 0
        if buyer_location=="":
            self.login_text="Please Enter your Location"
            return 0
        if buyer_phone=="":
            self.login_text="Please Enter your Phone number"
            return 0


        email_validator=self.creater.validate_email(buyer_email)
        if email_validator == 0:
            print("Invalid email address")
            self.login_text="Invalid email address"
            return 0
        password_validator= self.creater.validate_password(buyer_password)
        if password_validator == 0:
            print("Wrong password. Please enter the password attributed to your GrabNGo account")
            self.login_text="Wrong password.\nPlease enter a Stong password"
            return 0
        validator  = self.creater.create_buyer_account(buyer_name,buyer_email,buyer_location,buyer_phone,buyer_password,self.date)
        if validator:
            print("Account has been created")
            self.login_text="Account has been created"
            self.ids.buyer_create_account_name.text =""
            self.ids.buyer_create_account_email.text=""
            self.ids.buyer_create_account_password.text=""
            self.ids.buyer_create_account_location.text=""
            self.ids.buyer_create_account_phone.text=""

            App.get_running_app().buyer_name=buyer_name
            App.get_running_app().buyer_id = self.creater.get_buyer_id(App.get_running_app().buyer_name)
            App.get_running_app().buyer_location = buyer_location
            App.get_running_app().buyer_password = buyer_password 
            App.get_running_app().buyer_email = buyer_email
            App.get_running_app().buyer_phone = buyer_phone

            self.manager.current = "buyerdashboard"
            

        else:
            print(validator)
            self.login_text=validator


# ===============================
# CREATE SELLER ACCOUNT
# ===============================
class Create_Seller_Account_Page(Screen):
    login_text=StringProperty("")
    def get_formatted_date(self):
    	# This returns the current date in the exact DD-MM-YY format
        return datetime.now().strftime("%d-%m-%y")

    def seller_create_account(self):
        self.creater=Seller_Login(con)
        self.date=self.get_formatted_date()
        seller_name= (self.ids.seller_create_accuont_name.text).strip()
        seller_email=(self.ids.seller_create_account_email.text).strip()
        seller_password=(self.ids.seller_create_account_password.text).strip()
        seller_location=(self.ids.seller_create_account_location.text).strip()
        seller_phone=(self.ids.seller_create_account_phone.text).strip()
        if seller_name=="":
            self.login_text="Please Enter your UserName"
            return 0
        if seller_email=="":
            self.login_text="Please Enter your Email"
            return 0
        if seller_password=="":
            self.login_text="Please Enter your Password"
            return 0
        if seller_location=="":
            self.login_text="Please Enter your Location"
            return 0
        if seller_phone=="":
            self.login_text="Please Enter your Phone number"
            return 0

        email_validator=self.creater.validate_email(str(seller_email))
        if email_validator == 0:
            print("Invalid email address")
            login_text="Invalid email address"
            return 0
        password_validator= self.creater.validate_password(seller_password)
        if password_validator == 0:
            print("Wrong password. Please enter a strong pasword")
            login_text="Wrong password. Please enter the password attributed to your GrabNGo account"
            return 0
        b_name=""
        b_type=""
        open_time=""
        rat=0
        number_of_sales=0
        image=""

        self.creater.create_seller_account(name=seller_name,buisness_name=b_name,buisness_type=b_type,phone=seller_phone,e_mail=seller_email,password=seller_password,location=seller_location,open_time=open_time,rating=rat,number_of_sales=number_of_sales,date_of_creation=self.date,img=image)
        print("Account has been created")
        self.login_text="Account has been created"
        self.ids.seller_create_accuont_name.text=""
        self.ids.seller_create_account_email.text=""
        self.ids.seller_create_account_password.text=""
        self.ids.seller_create_account_location.text=""
        self.ids.seller_create_account_phone.text=""


        App.get_running_app().seller_name=seller_name
        App.get_running_app().seller_email=seller_email
        App.get_running_app().seller_password=seller_password
        App.get_running_app().seller_location=seller_location
        App.get_running_app().seller_phone=seller_phone
        self.manager.current = "seller_manager_page"



# ===============================
# BUYER DASHBOARD
# ===============================
class BusinessCard(BoxLayout):
    biz_name = StringProperty()
    biz_type = StringProperty()
    biz_location = StringProperty()
    biz_rating = StringProperty()
    biz_logo = StringProperty()


class BuyerDashboard(Screen):
    def on_enter(self):
        print("*****************************")
        print(App.get_running_app().buyer_name)
        print("*****************************")
        Clock.schedule_once(self.load_sellers, 0)

    def load_sellers(self, dt):
        Manager = Buyer_Search_Transactions(con,App.get_running_app().buyer_name)
        sellers = Manager.Get_sellers()

        self.ids.rv.data = [{
            "biz_name": s[2],
            "biz_type": s[3],
            "biz_location": s[7],
            "biz_rating": str(s[9]),
            "seller_name":s[1],
            "biz_logo": s[12] or "logo.png"
        } for s in sellers]

    def visit_seller(self, name, loc):
        Manager = Buyer_Search_Transactions(con,App.get_running_app().buyer_name)
        App.get_running_app().is_active=False
        App.get_running_app().seller_name = name
        App.get_running_app().seller_id = Manager.find_seller_id(App.get_running_app().seller_name)
        App.get_running_app().seller_location = loc
        self.manager.current = "storepage"

    def load_user_profile(self):
        self.manager.current = "buyer_profile_page"


    def load_cart(self):
        self.manager.current = "cartpage"



# ===============================
# STORE PAGE
# ===============================
class ProductCard(BoxLayout):
    p_name = StringProperty("")
    p_price = NumericProperty(0)
    p_desc = StringProperty("")
    p_img = StringProperty("logo.png")
    seller_name = StringProperty("")
    seller_loc = StringProperty("")
    qty=NumericProperty(0)


class StorePage(Screen):
    seller_name = StringProperty("")
    seller_loc = StringProperty("")
    seller_id=NumericProperty(0)
    qty=NumericProperty(1)
    


    p_name = StringProperty("")
    p_cat = StringProperty("")
    p_desc = StringProperty("")
    p_price = StringProperty("")
    def on_enter(self):
        Clock.schedule_once(self.load_seller_products, 0)

    def load_seller_products(self, dt):
        self.seller_name=App.get_running_app().seller_name
        Manager = Buyer_Visit_Seller(con, "Bob")
        products = Manager.visit_sellers(self.seller_name)
        if products == None:
            return 0
        self.ids.product_rv.data = [{
            "p_name": p[1],
            "p_desc": p[2],
            "p_price": str(p[4]),
            "p_img": p[6] or "logo.png",
            "seller_name":self.seller_name,
            "qty":self.qty
        } for p in products]

    def load_user_profile(self):
        self.manager.current = "buyer_profile_page"

    def load_cart(self):
        self.manager.current = "cartpage"
    def buy_product(self,p_name,s_name,qty):
        print("buying in progress")
        buying_manager=Buyer_Cart_Manager(con,App.get_running_app().buyer_name,App.get_running_app().buyer_location)
        buying_manager.place_order(p_name,s_name,qty)
        App.get_running_app().product_bought[p_name]=qty
        print(App.get_running_app().product_bought)
        print("buying terminated")

    def get_product_info(self,name):
        print("00000000000000000000000")
        print(name, self.seller_name)
        Manager = Buyer_Search_Transactions(con,App.get_running_app().buyer_name)
        info=Manager.get_product_detail(name,self.seller_name)
        print(info)
        self.p_price=str(info[0][2])
        self.p_des=info[0][0]
        self.p_cat=info[0][1]
        self.p_name=name
        popup = ProductInfoPopup()
        popup.open()
        
                 
            


class CartItem(BoxLayout):
    product_name = StringProperty("")
    product_price = NumericProperty(0)
    product_qty = NumericProperty(0)
    seller_name= StringProperty("")
    order_id= NumericProperty(0)
    index= NumericProperty(0)


# ===============================
# CART PAGE (BUG FIXED)
# ===============================
class CartPage(Screen):
    total_sum = NumericProperty(0.0)

    def on_enter(self):
        Clock.schedule_once(self._load_cart_safe, 0)

    def _load_cart_safe(self, dt):
        self.load_cart_data()
        self.compute_sum_action()

    def load_cart_data(self):
        manager = Buyer_Cart_Manager(
            con,
            App.get_running_app().buyer_name,
            App.get_running_app().buyer_location
        )
        cart_data = manager.view_cart()
        if not cart_data:
            self.ids.cart_rv.data = []
            self.total_sum = 0
            return
        for item in cart_data:
            App.get_running_app().order_ids.append(item[0])
        self.ids.cart_rv.data = [{
            "product_name": row[1],
            "product_price": str(row[3]),
            "product_qty": str(row[4]),
            "seller_name":row[2],
            "order_id":row[0],
            "index":i
        } for i, row in enumerate(cart_data)]

    def compute_sum_action(self):
        manager = Buyer_Cart_Manager(
            con,
            App.get_running_app().buyer_name,
            App.get_running_app().buyer_location
        )
        cart_data = manager.view_cart()

        if not cart_data:
            self.total_sum = 0
            return

        self.total_sum = sum(float(i[3]) * int(i[4]) for i in cart_data)

    def update_qty(self, ID,QTY):
        Manager = Buyer_Cart_Manager(
            con,
            App.get_running_app().buyer_name,
            App.get_running_app().buyer_location
        )
        Manager.update_buyer_product_qty( ID,QTY)
        self.load_cart_data()
        self.compute_sum_action()       


    def delete_item(self, ID):
        manager = Buyer_Cart_Manager(
            con,
            App.get_running_app().buyer_name,
            App.get_running_app().buyer_location
        )
        manager.delete_from_cart(ID)
        self.load_cart_data()
        self.compute_sum_action()       
    def clear_cart(self):
        manager = Buyer_Cart_Manager(
            con,
            App.get_running_app().buyer_name,
            App.get_running_app().buyer_location
        )
        manager.empty_cart()
        self.load_cart_data()
        self.compute_sum_action()       

class QuantityPopup(ModalView):
    p_name = StringProperty("")
    order_id=NumericProperty(0)

class BuyerLocationPopup(ModalView):
    location = StringProperty("")
    order_id=NumericProperty(0)

class ProductInfoPopup(ModalView):
    print("Ermmmmmm this guy is suppose to be working")
class AddProductPopup(ModalView):
    product_name=StringProperty("")
    description=StringProperty("")
    category=StringProperty("")
    price=NumericProperty(0)
    qty=NumericProperty(0)
    img=StringProperty("")


class UpdateProductPopup(ModalView):
    # Properties to hold the initial data
    p_name = StringProperty("")
    p_desc = StringProperty("")
    p_price = StringProperty("")
    p_cat = StringProperty("")
    p_qty = StringProperty("")
    p_img = StringProperty("")
    
    # We store the original name to use as a key for the SQL query
    old_name = StringProperty("")

    def apply_update(self):
        app = App.get_running_app()
        # Access the Screen class where your update_product logic lives
        screen = app.root.get_screen('seller_manager_page')
        
        # Call your backend logic with all required arguments
        screen.update_product(
            self.ids.product_name.text,   # new name
            self.ids.description.text,    # des
            self.ids.category.text,       # cat
            self.ids.price.text,          # price
            self.ids.qty.text,            # qty
            self.ids.img.text,            # img
            self.old_name,                # Name (original name for WHERE clause)
            app.seller_name               # s_name
        )
        self.dismiss()



class UpdateSellerInfoPopup(ModalView):
    # Properties to hold the initial data
    biz_name = StringProperty("")
    biz_type = StringProperty("")
    loc = StringProperty("")
    o_time = StringProperty("")
    pic = StringProperty("")
    
    # We store the original name to use as a key for the SQL query
    old_name = StringProperty("")

    def apply_update(self):
        app = App.get_running_app()
        # Access the Screen class where your update_product logic lives
        screen = app.root.get_screen('seller_profile_page')
        
        # Call your backend logic with all required arguments
        screen.update_info(
            self.ids.buisness_name.text,   # new name
            self.ids.buisness_type.text,    # des
            self.ids.buisness_location.text,       # cat
            self.ids.open_time.text,          # price
            self.ids.profile.text,            # qty
        )
        self.dismiss()


# ===============================
# PAYMENT + REVIEW
# ===============================

class PaymentPage(Screen):
    total_sum = NumericProperty(0.0)

    def on_enter(self):
        cart = self.manager.get_screen('cartpage')
        self.total_sum = cart.total_sum

    def process_payment(self):
        print("Payment Successful!")
        payer=Buyer_Payment_Transactions(con,App.get_running_app().buyer_name,App.get_running_app().buyer_location)
        cart = self.manager.get_screen('cartpage')
        print("This are all the product bought:   ")
        print(App.get_running_app().product_bought)
        for product in App.get_running_app().product_bought:
            print("reudcing the stocks")
            payer.reduce_stock_of_purchase_items(product,App.get_running_app().seller_name,App.get_running_app().product_bought[product])

        
        agent_name=payer.asign_delivery_agent(App.get_running_app().seller_name,App.get_running_app().order_ids[0])
        agent_name=agent_name[0]
        print("This is the free delivery agent:    ")
        print(agent_name)
        print("Now populating the agent")
        for item in App.get_running_app().order_ids:
            payer.populate_delivery_agent(item,agent_name)
        App.get_running_app().approximate_time=str(payer.get_delivery_time(App.get_running_app().seller_location))
        if App.get_running_app().approximate_time==0:
            App.get_running_app().approximate_time="Please Contact Seller to get the Aproximate Delivery time"
        print("This is the approximate time:   "+App.get_running_app().approximate_time)
        self.manager.current = 'review_page'

    def back_to_cart(self):
        self.manager.current = 'cartpage'


class Review_Page(Screen):
    response_to_wrong_rating=StringProperty("")
    def submit_review(self, rat):
        if not rat.isdigit() or not (1 <= int(rat) <= 5):
            self.response_to_wrong_rating = "INVALID INPUT: CHOOSE 1-5"
            return
        
        reviewer=Buyer_Submit_Review(con,App.get_running_app().buyer_name)
        print("Now inserint into history and also deleting from the orders table")
        for order in App.get_running_app().order_ids:

            reviewer.insert_into_history(order,datetime.now().strftime("%d-%m-%y"))
            reviewer.delete_from_orders(order)
        self.manager.current = "buyerdashboard"
        print("Updating review")
        reviewer.update_rating(App.get_running_app().seller_id,int(rat))

    def skip_review(self):
        self.manager.current = "buyerdashboard"
        
# ===============================
# PAYMENT + REVIEW
# ===============================
class Delivery_Agent_Login_Page(Screen):
    agent_login_text=StringProperty("")

    def Delivery_agent_Loginto_app(self):
        Agent_name= (self.ids.delivery_agent_name.text).strip()
        Agent_id=(self.ids.delivery_agent_id.text).strip()
        Agent_location=(self.ids.delivery_agent_location.text).strip()

        if Agent_name=="":
            self.agent_login_text="Please Enter your UserName"
            return 0
        
        if Agent_id=="":
            self.agent_login_text="Please Enter your the personal ID\nissued to you by your Seller_Admin"
            return 0
        if not Agent_id.isdigit():
            self.agent_login_text="Please Enter a Number as Agent ID"
            return 0

        if Agent_location=="":
            self.agent_login_text="Please Enter your location"
            return 0

        manager1=Agent_Login(con)
        logingin=manager1.login(Agent_name,int(Agent_id))
        print(logingin)
        if logingin:
            self.agent_login_text="Login sucessfull"

            self.ids.delivery_agent_name.text=""
            self.ids.delivery_agent_id.text=""
            self.ids.delivery_agent_location.text=""

            App.get_running_app().agent_name=Agent_name
            App.get_running_app().agent_id=Agent_id
            App.get_running_app().agent_location=Agent_location

            self.manager.current = "agent_order_page"



        else:
            self.agent_login_text="Account not found"
            self.ids.delivery_agent_name.text=""
            self.ids.delivery_agent_id.text=""
            self.ids.delivery_agent_location.text=""



  



# ===============================
# PAYMENT + REVIEW
# ===============================
class Buyer_Profile_Page(Screen):
    buyer_name_label = StringProperty("")
    def on_enter(self):
        app = App.get_running_app()
        if app.buyer_name:
            self.account_manager = Buyer_Account_Manager(con,App.get_running_app().buyer_name)
            info = self.account_manager.get_buyer_info()
            self.buyer_name=info[0][1]
            self.buyer_email=info[0][2]
            self.buyer_password=info[0][5]
            self.buyer_location=info[0][3]
            self.buyer_phone=info[0][4]

    def update_location(self,location):
        self.account_manager = Buyer_Account_Manager(con,App.get_running_app().buyer_name)
        self.account_manager.change_location(location)
        app = App.get_running_app()
        app.buyer_name=location
        if app.buyer_name:
            self.account_manager = Buyer_Account_Manager(con,App.get_running_app().buyer_name)
            info = self.account_manager.get_buyer_info()
            self.buyer_name=info[0][1]
            self.buyer_email=info[0][2]
            self.buyer_password=info[0][5]
            self.buyer_location=info[0][3]
            self.buyer_phone=info[0][4]

    def delete_buyer_account(self):
        self.account_manager = Buyer_Account_Manager(con,App.get_running_app().buyer_name)
        self.account_manager.delete_account()
        self.manager.current = "first_page"
        
# ===============================
# PAYMENT + REVIEW
# ===============================
    
class Seller_Profile_Page(Screen):
    buisness_name=StringProperty("")
    buizness_type=StringProperty("")
    seller_location=StringProperty("")
    seller_opening_time=StringProperty("")
    pic=StringProperty("")

    def on_enter(self):
        app = App.get_running_app()
        
        if app.seller_name:
            self.Manager = Seller_Account_Manager(con, App.get_running_app().seller_name)  
            info=self.Manager.Get_seller_info()          
            self.seller_name=info[0][1]
            self.seller_email=info[0][5]
            self.seller_password=info[0][6]
            self.seller_location=info[0][7]
            self.seller_phone=info[0][4]
            self.buisness_name=info[0][2]
            self.buisness_type=info[0][3]
            self.seller_opening_time=info[0][8]
            self.seller_number_of_sales=info[0][10]
            self.pic=info[0][12]
            self.seller_rating=float(info[0][9])

    def open_seller_info_update_popup(self):
        popup = UpdateSellerInfoPopup()
        # Transfer data to popup
        popup.biz_name = self.buisness_name
        popup.biz_type = self.buisness_type
        popup.loc = self.seller_location
        popup.o_time = self.seller_opening_time
        popup.pic = self.pic
        popup.open()

    def update_info(self,name,type,location,time,pic):
        updater=Seller_Account_Manager(con,App.get_running_app().seller_name)
        updater.change_buisness(name,type,location,time,pic)
        self.on_enter()



# ===============================
# PAYMENT + REVIEW
# ===============================
from kivy.properties import StringProperty # Ensure this is imported

class Get_Store_Annalytic_Page(Screen):
    # --- SEMANTIC FIX: YOU MUST DECLARE THESE HERE ---
    daily_income = StringProperty("0")
    weekly_income = StringProperty("0")
    monthly_income = StringProperty("0")
    yearly_income = StringProperty("0")
    most_sold_product = StringProperty("")
    max_qty = StringProperty("0")
    least_sold_product = StringProperty("")
    min_qty = StringProperty("0")

    def on_enter(self):
        Clock.schedule_once(self.initialize_seller_data, 0)

    def initialize_seller_data(self, dt):
        app = App.get_running_app()
        if app.seller_name:
            # Using self.manager ensures it's available to the whole class
            self.manager = Seller_Store_Manager(con, app.seller_name)
            
            # Updating these Kivy Properties now triggers the KV UI update
            self.daily_income = str(self.manager.calculate_daily_income())
            self.weekly_income = str(self.manager.calculate_weekly_income())
            self.monthly_income = str(self.manager.calculate_monthly_income())
            self.yearly_income = str(self.manager.calculate_yearly_income())

            stat = self.manager.seller_statistics()
            print("*************&&&&&&&&*********")
            print(stat)
            print("*************&&&&&&&&*********")

            if stat and len(stat) >= 4:
                print("as;dkgljjjjjjjjjjjjjjjjjjjjj")
                self.most_sold_product = stat[0]
                self.max_qty = str(stat[1])
                self.least_sold_product = stat[2]
                self.min_qty = str(stat[3])
            else:
                self.most_sold_product = "None"
                self.max_qty = "0"
                self.least_sold_product = "None"
                self.min_qty = "0"


class SellerProductCard(BoxLayout):
    p_name = StringProperty("")
    p_price = StringProperty("")
    p_desc = StringProperty("")
    p_img = StringProperty("logo.png")
    # Add these to match your backend requirements
    p_cat = StringProperty("")
    p_qty = StringProperty("")

    def open_edit_popup(self):
        popup = UpdateProductPopup()
        # Transfer data to popup
        popup.p_name = self.p_name
        popup.old_name = self.p_name # Store the original name here
        popup.p_desc = self.p_desc
        popup.p_price = self.p_price.replace("CFA ", "") # Clean price for numeric input
        popup.p_cat = self.p_cat
        popup.p_qty = self.p_qty
        popup.p_img = self.p_img
        popup.open()
# ===============================
# PAYMENT + REVIEW
# ===============================
class Seller_Manager_Page(Screen):
    def on_enter(self):
        # Use Clock to ensure IDs are assigned before loading
        print("sadddddddddddddddddddddddg")
        self.p_name = StringProperty("")
        self.p_price = StringProperty("")
        self.p_desc = StringProperty("")
        self.p_img = StringProperty("logo.png")

        Clock.schedule_once(lambda dt: self.load_seller_products())

    def load_seller_products(self):
        try:
            self.seller_pic="logo.png"
            print("MMMMMMMMMMMMMMMMM")
            print(App.get_running_app().seller_name)
            manager =   Seller_View(con, App.get_running_app().seller_name)

            # Use dynamic name instead of hardcoded "Marie Ngo"
            all_product_data = manager.view_store() 
            print(all_product_data)
            print("dfhhhhhhhhasasssssssjhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhs") 
            if not all_product_data:
                self.ids.seller_product_rv.data = []
                return

            formatted = []
            for item in all_product_data:
                formatted.append({
                    'p_name': str(item[1]),
                    'p_desc': str(item[2]),
                    'p_cat': str(item[3]),
                    'p_price': str(item[4]),
                    'p_qty': str(item[5]),
                    'p_img': str(item[6]) if (len(item) > 6 and item[6]) else "logo.png"
                })
            self.ids.seller_product_rv.data = formatted

        except Exception as e:
            print(f"Error in load_seller_products: {e}")

    def update_product(self,name,des,cat,price, qty,img,Name,s_name):
        updater=Seller_Store_Manager(con,App.get_running_app().seller_name)
        print(Name)
        ID=updater.get_product_id(Name)
        updater.update_product(des,cat,price, qty,img,ID,App.get_running_app().seller_id)
        Clock.schedule_once(lambda dt: self.load_seller_products())

    def add_product(self,name,description,category,price,qty,img):
        adder=Seller_Store_Manager(con,App.get_running_app().seller_name)
        adder.add_to_store(name,description,category,price,qty,img)
        Clock.schedule_once(lambda dt: self.load_seller_products())


    def delete_product(self, name):
        remover=Seller_Store_Manager(con,App.get_running_app().seller_name)
        remover.delete_product(name)
        Clock.schedule_once(lambda dt: self.load_seller_products())




# ===============================
# PAYMENT + REVIEW
# ===============================


class AgentCard(BoxLayout):
    a_id = StringProperty("") # Hidden ID for database reference
    a_name = StringProperty("")
    a_loc = StringProperty("")


class AgentOrderCard(BoxLayout):
    p_name = StringProperty("")
    b_name = StringProperty("")
    p_qty = StringProperty("")
    s_loc = StringProperty("")
    b_loc = StringProperty("")
class Delivery_Manager_Page(Screen):
    # ... your load_agents logic ...
    def on_enter(self):
        # Use Clock to ensure IDs are assigned before loading
        Clock.schedule_once(lambda dt: self.load_agents())
    
    def load_agents(self):
        # Sample data based on your "list of lists" [[id, name, location, status], ...]
        manager =  Seller_View(con, App.get_running_app().seller_name)

        all_agents = manager.view_delivery_agents()
        if all_agents == None:
            self.ids.agent_rv.data=[]
            return 0
        print("sadddddddddddddddddddddddg")
        print(all_agents)
        formatted = []
        for agent in all_agents:
            formatted.append({
                'a_id': str(agent[0]),    # Pass the ID here
                'a_name': str(agent[1]),
                'a_loc': str(manager.get_a_loc(agent[1]))
            }) 
        self.ids.agent_rv.data = formatted
        self.ids.agent_rv.refresh_from_data()
    def add_agent(self,name,location):
        if name=="" or location=="":
            return
        adder=Seller_Store_Manager(con,App.get_running_app().seller_name)
        adder.add_delivery_agent(name,location)
        self.load_agents()

    def delete_agent(self, agent_id, agent_name):
        print(f"Removing Agent ID: {agent_id} ({agent_name}) from records...")
        adder=Seller_Store_Manager(con,App.get_running_app().seller_name)
        adder.delete_delivery_agent(agent_name)
        self.load_agents() # Refresh the list


class HistoryItem(BoxLayout):
    """Visual row component"""
    product_name = StringProperty("")
    seller_name = StringProperty("")
    qty = StringProperty("")
    price = StringProperty("")
    date = StringProperty("")
    total_row = StringProperty("") # Calculated as Qty * Price


class SellerHistoryItem(BoxLayout):
    """Visual row component"""
    product_name = StringProperty("")
    qty = StringProperty("")
    price = StringProperty("")
    date = StringProperty("")
    delivery_agent_name = StringProperty("")
    total_row = StringProperty("")
    # Calculated as Qty * Price

class BuyerHistoryPage(Screen):
    def on_enter(self):
        # Trigger load every time screen is viewed
        Clock.schedule_once(self.load_history, 0)

    def load_history(self, dt):
        account_manager=Buyer_Account_Manager(con,App.get_running_app().buyer_name)
        raw_data = account_manager.view_buyer_history()

        if not raw_data:
            self.ids.history_rv.data = []
            return

        # 2. Map the list of lists to the RecycleView dictionary
        self.ids.history_rv.data = [{
            "product_name": str(row[1]),
            "seller_name": str(row[2]),
            "qty": str(row[3]),
            "price": str(row[4]),
            "date": str(row[5]),
            "total_row": str(float(row[3]) * float(row[4])) # Dynamic total
        } for row in raw_data]
        


class SellerHistoryPage(Screen):
    def on_enter(self):
        # Trigger load every time screen is viewed
        Clock.schedule_once(self.load_history, 0)
        print("Start\n")

    def load_history(self, dt):
        print("Start\n")

        account_manager=Seller_Account_Manager(con,App.get_running_app().seller_name)
        raw_data = account_manager.view_seller_history()
        print("Start\n")


        if not raw_data:
            self.ids.seller_history_rv.data = []
            return
        # 2. Map the list of lists to the RecycleView dictionary
        self.ids.seller_history_rv.data = [{
            "product_name": str(row[0]),
            "qty": str(row[1]),
            "price": str(row[2]),
            "date": str(row[3]),
            "delivery_agent_name": str(row[4]),
            "total_row": str(float(row[1]) * float(row[2])) # Dynamic total
        } for row in raw_data]

# ===============================
# PAYMENT + REVIEW
# ===============================
class Agent_Order_Page(Screen):
    def on_enter(self):
        # Refresh orders when agent opens the page
        print("**********************")
        Clock.schedule_once(lambda dt: self.load_agent_orders())

    def load_agent_orders(self):
        try:
            # Assuming get_orders() returns:
            # [[id, productname, buyername, ..., qty, ..., ..., ..., s_loc, b_loc]]
            # indices: [1] p_name, [2] b_name, [5] qty, [9] s_loc, [10] b_loc
            
            manager = delivery(con,App.get_running_app().agent_id)
            all_orders = manager.display_orders() 
            print(all_orders)
            
            if not all_orders:
                self.ids.agent_order_rv.data = []
                return

            formatted = []
            for order in all_orders:
                formatted.append({
                    'p_name': str(order[1]),
                    'b_name': str(order[2]),
                    'p_qty': str(order[5]),
                    's_loc': str(order[9]),
                    'b_loc': str(order[10])
                })
            self.ids.agent_order_rv.data = formatted
        except Exception as e:
            print(f"Error loading agent orders: {e}")

    def complete_delivery(self, product_name):
        print(f"Order for {product_name} marked as delivered!")
        self.load_agent_orders()

class ConfigureBuisnessPage(Screen):
    check_text = StringProperty("")
    answer_to_password_forgotten = StringProperty("")
    print("Tsuipppppppppppppp")

    def create_buiness(self):
        App.get_running_app().seller_name="Logan"
        self.configurer = Seller_Account_Manager(con,App.get_running_app().seller_name)
        print("*********************************")

        b_name = self.ids.biz_name.text.strip()
        b_type = self.ids.biz_type.text.strip()
        o_time = self.ids.open_time.text.strip()
        c_time = self.ids.close_time.text.strip()
        pic = self.ids.pic_path.text.strip()

        if not b_name:
            self.check_text = "Please Enter The Buisness Name"
            return
        if not b_type:
            self.check_text = "Please Enter Buisness Type"
            return
        if not o_time:
            self.check_text = "Please Enter The Opening Time"
            return

        if not c_time:
            self.check_text = "Please Enter The Clossing Time"
            return
        if not pic:
            self.check_text = "Please Provide a profile pic"
            return

        result = self.configurer.create_entire_buisness(b_name,b_type,o_time,pic)

        if result == 1:
            self.check_text = "Login in............"
            App.get_running_app().Buisness_name=b_name
            App.get_running_app().Buisness_name=b_type
            App.get_running_app().seller_opening_time=o_time
            App.get_running_app().seller_pic=pic

            self.manager.current = "seller_manager_page"
        else:
            self.login_text = str(result)

class SellerOrdersPage(Screen):
    orders_data = ListProperty([])

    def on_enter(self):
        self.fetch_seller_orders()

    def fetch_seller_orders(self):
        # viewer returns the list of lists from your backend
        viewer = Seller_View(con, App.get_running_app().seller_name)
        orders = viewer.view_orders() 
        
        # We must clear and rebuild the list for the RecycleView
        formatted_orders = []
        for row in orders:
            # Assuming your list index order: 
            # 0:ID, 1:Product, 3:Buyer, 5:Qty, 8:Agent, 9:Location
            formatted_orders.append({
                'order_id': str(row[0]),
                'product_name': str(row[1]),
                'buyer_name': str(row[3]),
                'quantity': str(row[5]),
                'agent_name': str(row[8]),
                'b_location': str(row[9]),
                'status': "PENDING" # Placeholder or row[index] if available
            })
            print(formatted_orders)
        
        self.orders_data = formatted_orders
    
    def manage_order(self):
        print("Opening control terminal for order:")

# ===============================
# APP
# ===============================
class GrabNGoApp(App):

    buisness_name = StringProperty()
    buisness_type = StringProperty()
    seller_location = StringProperty()
    seller_rating =NumericProperty()
    buisness_logo = StringProperty()
    seller_opening_time=StringProperty()
    seller_number_of_sales=NumericProperty()
    seller_name= StringProperty()
    seller_id= NumericProperty(0)
    seller_email = StringProperty()
    seller_phone=NumericProperty(0)
    seller_password=StringProperty()
    min_qty=NumericProperty(0)
    max_qty=NumericProperty(0)
    most_sold_product=StringProperty()
    least_sold_product=StringProperty()
    yearly_income=NumericProperty()
    monthly_income=NumericProperty()
    daily_income=NumericProperty()
    weekly_income=NumericProperty()
    seller_pic=StringProperty()
    total_sum = NumericProperty(0)
    is_active = BooleanProperty(True)
    product_bought=DictProperty({})
    order_ids=ListProperty([])



    buyer_name = StringProperty()
    buyer_id = NumericProperty(0)
    buyer_location = StringProperty()
    buyer_password=StringProperty()
    buyer_email = StringProperty()
    biz_logo = StringProperty()
    buyer_phone=NumericProperty(0)
    agent_name=StringProperty()
    agent_id=NumericProperty(0)
    agent_location=StringProperty()
    approximate_time=StringProperty()

  
    def build(self):
        screenmanager=ScreenManager(transition=SlideTransition())
        screenmanager.add_widget(First_Page(name="first_page"))
        screenmanager.add_widget(Buyer_Login_Page(name="buyer_login_page"))
        screenmanager.add_widget(Seller_Login_Page(name="seller_login_page"))
        screenmanager.add_widget(Delivery_Agent_Login_Page(name="delivery_agent_login_page"))
        screenmanager.add_widget(Create_Buyer_Account_Page(name="create_buyer_account_page"))
        screenmanager.add_widget(Create_Seller_Account_Page(name="create_seller_account_page"))
        screenmanager.add_widget(BuyerDashboard(name="buyerdashboard"))
        screenmanager.add_widget(Buyer_Profile_Page(name="buyer_profile_page"))
        screenmanager.add_widget(Seller_Profile_Page(name="seller_profile_page"))
        screenmanager.add_widget(Get_Store_Annalytic_Page(name="get_store_annalytic_page"))
        screenmanager.add_widget(StorePage(name="storepage"))
        screenmanager.add_widget(PaymentPage(name="paymentpage"))
        screenmanager.add_widget(CartPage(name="cartpage"))
        screenmanager.add_widget(Review_Page(name="review_page"))
        screenmanager.add_widget(Seller_Manager_Page(name="seller_manager_page"))
        screenmanager.add_widget(Delivery_Manager_Page(name="deliver_manager_page"))
        screenmanager.add_widget(Agent_Order_Page(name="agent_order_page"))
        screenmanager.add_widget(BuyerHistoryPage(name="buyerhistorypage"))
        screenmanager.add_widget(SellerHistoryPage(name="sellerhistorypage"))
        screenmanager.add_widget(ConfigureBuisnessPage(name="configurebuisnesspage"))
        screenmanager.add_widget(SellerOrdersPage(name="sellerorderspage"))

#        screenmanager.current="first_page"\
        screenmanager.current="first_page"

        return screenmanager


if __name__ == "__main__":
    GrabNGoApp().run()
