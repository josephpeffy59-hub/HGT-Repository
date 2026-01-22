# ===============================
# STANDARD IMPORTS
# ===============================
import os
import requests  # Required for API communication
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from datetime import datetime
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.properties import (
    StringProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    DictProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.recycleview import RecycleView

# ===============================
# API CONFIGURATION
# ===============================
BASE_URL = "http://127.0.0.1:8000"

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
        # Logic preserved: Reading from IDs
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

        # REQUEST REPLACING: result = self.Logs.login(...)
        try:
            payload = {"name": buyer_name, "email": buyer_email, "password": buyer_password}
            response = requests.post(f"{BASE_URL}/buyer/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                result = 1
                info = data.get("info") # API returns the SQL list of lists
            else:
                result = response.json().get("detail", "Invalid Credentials")
        except Exception as e:
            result = f"Connection Error: {e}"

        if result == 1:
            # info = self.Logs.Get_buyer_info(buyer_name) -> Now part of login response
            print(info)
            App.get_running_app().buyer_name = info[0][1]
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

        # REQUEST REPLACING: result = self.Logs.login(...)
        try:
            payload = {"name": seller_name, "email": seller_email, "password": seller_password}
            response = requests.post(f"{BASE_URL}/seller/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                result = 1
                info = data.get("info")
            else:
                result = response.json().get("detail", "Invalid Credentials")
        except Exception as e:
            result = f"Connection Error: {e}"

        if result == 1:
            self.login_text = "Login in............"
            print("************^^^&&&&&&&&&&^***********")
            print(info)
            App.get_running_app().seller_name = info[0][1]
            App.get_running_app().seller_email = info[0][5]
            App.get_running_app().seller_password = info[0][6]
            App.get_running_app().seller_location = info[0][7]
            App.get_running_app().seller_phone = info[0][4]
            App.get_running_app().seller_id = info[0][0]

            App.get_running_app().buisness_name = info[0][2]
            App.get_running_app().buisness_type = info[0][3]
            App.get_running_app().seller_opening_time = info[0][8]
            App.get_running_app().seller_rating = int(info[0][9])
            App.get_running_app().seller_number_of_sales = info[0][10]

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
    login_text = StringProperty("")
    
    def get_formatted_date(self):
        return datetime.now().strftime("%d-%m-%y")

    def buyer_create_account(self):
        self.date = self.get_formatted_date()
        buyer_name = (self.ids.buyer_create_account_name.text).strip()
        buyer_email = (self.ids.buyer_create_account_email.text).strip()
        buyer_password = (self.ids.buyer_create_account_password.text).strip()
        buyer_location = ((self.ids.buyer_create_account_location.text).strip()).lower()
        buyer_phone = (self.ids.buyer_create_account_phone.text).strip()

        if buyer_name == "":
            self.login_text = "Please Enter your UserName"
            return 0
        if buyer_email == "":
            self.login_text = "Please Enter your Email"
            return 0
        if buyer_password == "":
            self.login_text = "Please Enter your Password"
            return 0
        if buyer_location == "":
            self.login_text = "Please Enter your Location"
            return 0
        if buyer_phone == "":
            self.login_text = "Please Enter your Phone number"
            return 0

        try:
            # REQUEST REPLACING: email_validator = self.creater.validate_email(buyer_email)
            v_email_resp = requests.get(f"{BASE_URL}/validate/email", params={"email": buyer_email})
            email_validator = 1 if v_email_resp.json().get("valid") else 0

            if email_validator == 0:
                print("Invalid email address")
                self.login_text = "Invalid email address"
                return 0

            # REQUEST REPLACING: password_validator = self.creater.validate_password(buyer_password)
            v_pass_resp = requests.get(f"{BASE_URL}/validate/password", params={"password": buyer_password})
            password_validator = 1 if v_pass_resp.json().get("valid") else 0

            if password_validator == 0:
                print("Wrong password. Please enter the password attributed to your GrabNGo account")
                self.login_text = "Wrong password.\nPlease enter a Stong password"
                return 0

            # REQUEST REPLACING: validator = self.creater.create_buyer_account(...)
            create_payload = {
                "name": buyer_name, "email": buyer_email, "location": buyer_location,
                "phone": buyer_phone, "password": buyer_password, "date": self.date
            }
            create_resp = requests.post(f"{BASE_URL}/buyer/create", json=create_payload)
            create_data = create_resp.json()
            validator = create_data.get("result") # Returns 1 if successful

            resp = requests.get(f"{BASE_URL}/buyer/id",params={"name": App.get_running_app().buyer_name})

            buyer_id = resp.json()["buyer_id"]

            new_id = buyer_id

        except Exception as e:
            self.login_text = "Network Error"
            return 0

        if validator:
            print("Account has been created")
            self.login_text = "Account has been created"
            self.ids.buyer_create_account_name.text = ""
            self.ids.buyer_create_account_email.text = ""
            self.ids.buyer_create_account_password.text = ""
            self.ids.buyer_create_account_location.text = ""
            self.ids.buyer_create_account_phone.text = ""

            App.get_running_app().buyer_name = buyer_name
            # REQUEST REPLACING: App.get_running_app().buyer_id = self.creater.get_buyer_id(...)
            App.get_running_app().buyer_id = new_id
            App.get_running_app().buyer_location = buyer_location
            App.get_running_app().buyer_password = buyer_password 
            App.get_running_app().buyer_email = buyer_email
            App.get_running_app().buyer_phone = buyer_phone

            self.manager.current = "buyerdashboard"
        else:
            print(validator)
            self.login_text = str(validator)

# ===============================
# CREATE SELLER ACCOUNT
# ===============================
class Create_Seller_Account_Page(Screen):
    login_text = StringProperty("")
    
    def get_formatted_date(self):
        return datetime.now().strftime("%d-%m-%y")

    def seller_create_account(self):
        self.date = self.get_formatted_date()
        seller_name = (self.ids.seller_create_account_name.text).strip()
        seller_email = (self.ids.seller_create_account_email.text).strip()
        seller_password = (self.ids.seller_create_account_password.text).strip()
        seller_location = (self.ids.seller_create_account_location.text).strip()
        seller_phone = (self.ids.seller_create_account_phone.text).strip()
        
        if seller_name == "":
            self.login_text = "Please Enter your UserName"
            return 0
        if seller_email == "":
            self.login_text = "Please Enter your Email"
            return 0
        if seller_password == "":
            self.login_text = "Please Enter your Password"
            return 0
        if seller_location == "":
            self.login_text = "Please Enter your Location"
            return 0
        if seller_phone == "":
            self.login_text = "Please Enter your Phone number"
            return 0

        try:
            # REQUEST REPLACING: email_validator = self.creater.validate_email(...)
            v_email = requests.get(f"{BASE_URL}/validate/email", params={"email": seller_email}).json()
            email_validator = 1 if v_email.get("valid") else 0
            
            if email_validator == 0:
                print("Invalid email address")
                self.login_text = "Invalid email address"
                return 0
            
            # REQUEST REPLACING: password_validator = self.creater.validate_password(...)
            v_pass = requests.get(f"{BASE_URL}/validate/password", params={"password": seller_password}).json()
            password_validator = 1 if v_pass.get("valid") else 0
            
            if password_validator == 0:
                print("Wrong password. Please enter a strong pasword")
                self.login_text = "Wrong password. Please enter the password attributed to your GrabNGo account"
                return 0

            b_name = ""
            b_type = ""
            open_time = ""
            rat = 0
            number_of_sales = 0
            image = ""

            # REQUEST REPLACING: self.creater.create_seller_account(...)
            payload = {
                "name": seller_name, "buisness_name": b_name, "buisness_type": b_type,
                "phone": seller_phone, "e_mail": seller_email, "password": seller_password,
                "location": seller_location, "open_time": open_time, "rating": rat,
                "number_of_sales": number_of_sales, "date_of_creation": self.date, "img": image
            }
            requests.post(f"{BASE_URL}/seller/create", json=payload)
            
            print("Account has been created")
            self.login_text = "Account has been created"
            self.ids.seller_create_accuont_name.text = ""
            self.ids.seller_create_account_email.text = ""
            self.ids.seller_create_account_password.text = ""
            self.ids.seller_create_account_location.text = ""
            self.ids.seller_create_account_phone.text = ""
            resp = requests.get(f"{BASE_URL}/seller/id",params={"name": App.get_running_app().seller_name})

            seller_id = resp.json()["seller_id"]

            App.get_running_app().seller_name = seller_name
            App.get_running_app().seller_id = seller_id
            App.get_running_app().seller_email = seller_email
            App.get_running_app().seller_password = seller_password
            App.get_running_app().seller_location = seller_location
            App.get_running_app().seller_phone = seller_phone
            self.manager.current = "seller_manager_page"

        except Exception as e:
            self.login_text = "Server Error during registration"

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
        # REQUEST REPLACING: sellers = Manager.Get_sellers()
        try:
            response = requests.get(f"{BASE_URL}/sellers")
            sellers = response.json() if response.status_code == 200 else []
        except:
            sellers = []

        self.ids.rv.data = [{
            "biz_name": s[2],
            "biz_type": s[3],
            "biz_location": s[7],
            "biz_rating": str(s[9]),
            "seller_name": s[1],
            "biz_logo": s[12] or "logo.png"
        } for s in sellers]

    def visit_seller(self, name, loc):
        # REQUEST REPLACING: App.get_running_app().seller_id = Manager.find_seller_id(...)
        try:
            resp = requests.get(f"{BASE_URL}/seller/id", params={"name": name})
            s_id = resp.json().get("id", 0)
        except:
            s_id = 0

        App.get_running_app().is_active = False
        App.get_running_app().seller_name = name
        App.get_running_app().seller_id = s_id
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
    seller_id = NumericProperty(0)
    qty = NumericProperty(1)
    
    p_name = StringProperty("")
    p_cat = StringProperty("")
    p_desc = StringProperty("")
    p_price = StringProperty("")

    def on_enter(self):
        Clock.schedule_once(self.load_seller_products, 0)

    def load_seller_products(self, dt):
        self.seller_name = App.get_running_app().seller_name
        # REQUEST REPLACING: products = Manager.visit_sellers(self.seller_name)
        try:
            resp = requests.get(f"{BASE_URL}/products", params={"seller_name": self.seller_name})
            products = resp.json()
        except:
            products = None

        if products == None:
            return 0
        self.ids.product_rv.data = [{
            "p_name": p[1],
            "p_desc": p[2],
            "p_price": str(p[4]),
            "p_img": p[6] or "logo.png",
            "seller_name": self.seller_name,
            "qty": self.qty
        } for p in products]

    def load_user_profile(self):
        self.manager.current = "buyer_profile_page"

    def load_cart(self):
        self.manager.current = "cartpage"

    def buy_product(self, p_name, s_name, qty):
        print("buying in progress")
        # REQUEST REPLACING: buying_manager.place_order(p_name, s_name, qty)
        payload = {
            "buyer_name": App.get_running_app().buyer_name,
            "buyer_location": App.get_running_app().buyer_location,
            "product_name": p_name,
            "seller_name": s_name,
            "quantity": qty
        }
        try:
            requests.post(f"{BASE_URL}/order/place", json=payload)
        except:
            print("Failed to contact server for order")

        App.get_running_app().product_bought[p_name] = qty
        print(App.get_running_app().product_bought)
        print("buying terminated")

    def get_product_info(self, name):
        print("00000000000000000000000")
        print(name, self.seller_name)
        # REQUEST REPLACING: info = Manager.get_product_detail(name, self.seller_name)
        try:
            resp = requests.get(f"{BASE_URL}/product/detail", params={"p_name": name, "s_name": self.seller_name})
            info = resp.json()
        except:
            info = [["N/A", "N/A", 0]]

        print(info)
        self.p_price = str(info[0][2])
        self.p_desc = info[0][0]
        self.p_cat = info[0][1]
        self.p_name = name
        popup = ProductInfoPopup()
        popup.open()

class CartItem(BoxLayout):
    product_name = StringProperty("")
    product_price = NumericProperty(0)
    product_qty = NumericProperty(0)
    seller_name = StringProperty("")
    order_id = NumericProperty(0)
    index = NumericProperty(0)


# ===============================
# CART PAGE
# ===============================
class CartPage(Screen):
    total_sum = NumericProperty(0.0)

    def on_enter(self):
        Clock.schedule_once(self._load_cart_safe, 0)

    def _load_cart_safe(self, dt):
        self.load_cart_data()
        self.compute_sum_action()

    def load_cart_data(self):
        # REQUEST REPLACING: manager.view_cart()
        try:
            params = {
                "buyer_name": App.get_running_app().buyer_name,
                "location": App.get_running_app().buyer_location
            }
            response = requests.get(f"{BASE_URL}/cart", params=params)
            cart_data = response.json() if response.status_code == 200 else []
        except:
            cart_data = []

        if not cart_data:
            self.ids.cart_rv.data = []
            self.total_sum = 0
            return
        App.get_running_app().order_ids.clear()
        for item in cart_data:
            App.get_running_app().order_ids.append(item[0])
            
        self.ids.cart_rv.data = [{
            "product_name": row[1],
            "product_price": str(row[3]),
            "product_qty": str(row[4]),
            "seller_name": row[2],
            "order_id": row[0],
            "index": i
        } for i, row in enumerate(cart_data)]

    def compute_sum_action(self):
        try:
            params = {"buyer_name": App.get_running_app().buyer_name}
            response = requests.get(f"{BASE_URL}/cart", params=params)
            cart_data = response.json() if response.status_code == 200 else []
        except:
            cart_data = []

        if not cart_data:
            self.total_sum = 0
            return

        self.total_sum = sum(float(i[3]) * int(i[4]) for i in cart_data)

    def update_qty(self, ID, QTY):
        try:
            requests.post(f"{BASE_URL}/cart/update", json={"order_id": ID, "qty": QTY})
        except:
            print("Failed to update qty on server")
            
        self.load_cart_data()
        self.compute_sum_action()

    def delete_item(self, ID):
        json={"buyer_name": App.get_running_app().buyer_name,"location": App.get_running_app().buyer_location,"order_id": ID}

        try:
            requests.post(f"{BASE_URL}/cart/delete", json={"order_id": ID})
        except:
            print("Failed to delete item on server")
            
        self.load_cart_data()
        self.compute_sum_action()

    def clear_cart(self):
        try:
            requests.post(f"{BASE_URL}/cart/clear", json={"buyer_name": App.get_running_app().buyer_name})
        except:
            print("Failed to clear cart on server")
            
        self.load_cart_data()
        self.compute_sum_action()


# ===============================
# POPUPS (NO MODIFICATIONS MADE)
# ===============================
class QuantityPopup(ModalView):
    p_name = StringProperty("")
    order_id = NumericProperty(0)


class BuyerLocationPopup(ModalView):
    location = StringProperty("")
    order_id = NumericProperty(0)


class ProductInfoPopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Ermmmmmm this guy is suppose to be working")


class AddProductPopup(ModalView):
    product_name = StringProperty("")
    description = StringProperty("")
    category = StringProperty("")
    price = NumericProperty(0)
    qty = NumericProperty(0)
    img = StringProperty("")


class UpdateProductPopup(ModalView):
    p_name = StringProperty("")
    p_desc = StringProperty("")
    p_price = StringProperty("")
    p_cat = StringProperty("")
    p_qty = StringProperty("")
    p_img = StringProperty("")
    old_name = StringProperty("")

    def apply_update(self):
        app = App.get_running_app()
        screen = app.root.get_screen('seller_manager_page')
        screen.update_product(
            self.ids.product_name.text,
            self.ids.description.text,
            self.ids.category.text,
            self.ids.price.text,
            self.ids.qty.text,
            self.ids.img.text,
            self.old_name,
            app.seller_name
        )
        self.dismiss()


class UpdateSellerInfoPopup(ModalView):
    biz_name = StringProperty("")
    biz_type = StringProperty("")
    loc = StringProperty("")
    o_time = StringProperty("")
    pic = StringProperty("")
    old_name = StringProperty("")

    def apply_update(self):
        app = App.get_running_app()
        screen = app.root.get_screen('seller_profile_page')
        screen.update_info(
            self.ids.buisness_name.text,
            self.ids.buisness_type.text,
            self.ids.buisness_location.text,
            self.ids.open_time.text,
            self.ids.profile.text,
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
        print("This are all the product bought:   ")
        print(App.get_running_app().product_bought)
        
        try:
            for product in App.get_running_app().product_bought:
                print("reudcing the stocks")
                payload = {
                    "product": product,
                    "seller": App.get_running_app().seller_name,
                    "qty": App.get_running_app().product_bought[product]
                }
                requests.post(f"{BASE_URL}/inventory/reduce", json=payload)

            resp = requests.post(f"{BASE_URL}/delivery/assign", json={
                "seller_name": App.get_running_app().seller_name,
                "order_id": App.get_running_app().order_ids[0]
            })
            agent_name = resp.json().get("agent_name", "None")
            
            print("This is the free delivery agent:     ")
            print(agent_name)
            print("Now populating the agent")
            
            for item in App.get_running_app().order_ids:
                requests.post(f"{BASE_URL}/delivery/populate", json={"order_id": item, "agent_name": agent_name})
            
            time_resp = requests.get(f"{BASE_URL}/delivery/time", params={"location": App.get_running_app().seller_location})
            App.get_running_app().approximate_time = str(time_resp.json().get("time", "0"))
            
        except Exception as e:
            print(f"Payment logic failed: {e}")

        if App.get_running_app().approximate_time == "0":
            App.get_running_app().approximate_time = "Please Contact Seller to get the Aproximate Delivery time"
        
        print("This is the approximate time:   " + App.get_running_app().approximate_time)
        self.manager.current = 'review_page'

    def back_to_cart(self):
        self.manager.current = 'cartpage'


class Review_Page(Screen):
    response_to_wrong_rating = StringProperty("")

    def submit_review(self, rat):
        if not rat.isdigit() or not (1 <= int(rat) <= 5):
            self.response_to_wrong_rating = "INVALID INPUT: CHOOSE 1-5"
            return
        
        print("Now inserint into history and also deleting from the orders table")
        try:
            date_str = datetime.now().strftime("%d-%m-%y")
            for order in App.get_running_app().order_ids:
                requests.post(f"{BASE_URL}/order/finalize", json={"order_id": order, "date": date_str})
                
            print("Updating review")
            requests.post(f"{BASE_URL}/seller/rate", json={
                "seller_id": App.get_running_app().seller_id,
                "rating": int(rat)
            })
        except:
            print("Review submission failed")
            
        self.manager.current = "buyerdashboard"

    def skip_review(self):
        self.manager.current = "buyerdashboard"


# ===============================
# DELIVERY AGENT LOGIN
# ===============================
class Delivery_Agent_Login_Page(Screen):
    agent_login_text = StringProperty("")

    def Delivery_agent_Loginto_app(self):
        Agent_name = (self.ids.delivery_agent_name.text).strip()
        Agent_id = (self.ids.delivery_agent_id.text).strip()
        Agent_location = (self.ids.delivery_agent_location.text).strip()

        if Agent_name == "":
            self.agent_login_text = "Please Enter your UserName"
            return 0
        
        if Agent_id == "":
            self.agent_login_text = "Please Enter your the personal ID\nissued to you by your Seller_Admin"
            return 0
        if not Agent_id.isdigit():
            self.agent_login_text = "Please Enter a Number as Agent ID"
            return 0

        if Agent_location == "":
            self.agent_login_text = "Please Enter your location"
            return 0

        # REQUEST REPLACING: logingin = manager1.login(Agent_name, int(Agent_id))
        try:
            response = requests.post(f"{BASE_URL}/agent/login", json={
                "name": Agent_name,
                "id": int(Agent_id)
            })
            logingin = response.json().get("success", False)
        except:
            logingin = False
            self.agent_login_text = "Connection Error"

        print(logingin)
        if logingin:
            self.agent_login_text = "Login sucessfull"

            self.ids.delivery_agent_name.text = ""
            self.ids.delivery_agent_id.text = ""
            self.ids.delivery_agent_location.text = ""

            App.get_running_app().agent_name = Agent_name
            App.get_running_app().agent_id = Agent_id
            App.get_running_app().agent_location = Agent_location

            self.manager.current = "agent_order_page"
        else:
            self.agent_login_text = "Account not found"
            self.ids.delivery_agent_name.text = ""
            self.ids.delivery_agent_id.text = ""
            self.ids.delivery_agent_location.text = ""


# ===============================
# BUYER PROFILE
# ===============================
class Buyer_Profile_Page(Screen):
    buyer_name_label = StringProperty("")
    
    def on_enter(self):
        app = App.get_running_app()
        if app.buyer_name:
            # REQUEST REPLACING: info = self.account_manager.get_buyer_info()
            try:
                response = requests.get(f"{BASE_URL}/buyer/info", params={"name": app.buyer_name})
                info = response.json() # Returns list of lists
                self.buyer_name = info[0][1]
                self.buyer_email = info[0][2]
                self.buyer_password = info[0][5]
                self.buyer_location = info[0][3]
                self.buyer_phone = info[0][4]
            except:
                print("Error fetching buyer profile")

    def update_location(self, location):
        # REQUEST REPLACING: self.account_manager.change_location(location)
        try:
            requests.post(f"{BASE_URL}/buyer/update_location", json={
                "name": App.get_running_app().buyer_name,
                "location": location
            })
        except:
            print("Failed to update location")

        app = App.get_running_app()
        app.buyer_name = location
        if app.buyer_name:
            # Logic preserved: Refetching info after update
            try:
                response = requests.get(f"{BASE_URL}/buyer/info", params={"name": app.buyer_name})
                info = response.json()
                self.buyer_name = info[0][1]
                self.buyer_email = info[0][2]
                self.buyer_password = info[0][5]
                self.buyer_location = info[0][3]
                self.buyer_phone = info[0][4]
            except:
                pass

    def delete_buyer_account(self):
        # REQUEST REPLACING: self.account_manager.delete_account()
        try:
            requests.post(f"{BASE_URL}/buyer/delete", json={"name": App.get_running_app().buyer_name})
        except:
            print("Failed to delete account")
        self.manager.current = "first_page"


# ===============================
# SELLER PROFILE
# ===============================
class Seller_Profile_Page(Screen):
    buisness_name = StringProperty("")
    buizness_type = StringProperty("")
    seller_location = StringProperty("")
    seller_opening_time = StringProperty("")
    pic = StringProperty("")

    def on_enter(self):
        app = App.get_running_app()
        if app.seller_name:
            # REQUEST REPLACING: info = self.Manager.Get_seller_info()
            try:
                response = requests.get(f"{BASE_URL}/seller/info", params={"name": app.seller_name})
                info = response.json()
                self.seller_name = info[0][1]
                self.seller_email = info[0][5]
                self.seller_password = info[0][6]
                self.seller_location = info[0][7]
                self.seller_phone = info[0][4]
                self.buisness_name = info[0][2]
                self.buisness_type = info[0][3]
                self.seller_opening_time = info[0][8]
                self.seller_number_of_sales = info[0][10]
                self.pic = info[0][12]
                self.seller_rating = float(info[0][9])
            except:
                print("Error fetching seller profile")

    def open_seller_info_update_popup(self):
        popup = UpdateSellerInfoPopup()
        popup.biz_name = self.buisness_name
        popup.biz_type = self.buisness_type
        popup.loc = self.seller_location
        popup.o_time = self.seller_opening_time
        popup.pic = self.pic
        popup.open()

    def update_info(self, name, type, location, time, pic):
        # REQUEST REPLACING: updater.change_buisness(...)
        try:
            requests.post(f"{BASE_URL}/seller/update_profile", json={
                "current_name": App.get_running_app().seller_name,
                "biz_name": name,
                "biz_type": type,
                "location": location,
                "time": time,
                "pic": pic
            })
        except:
            print("Failed to update seller info")
        self.on_enter()


# ===============================
# STORE ANALYTICS
# ===============================
class Get_Store_Annalytic_Page(Screen):
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
            # REQUEST REPLACING: self.manager.calculate_income() and seller_statistics()
            try:
                response = requests.get(f"{BASE_URL}/seller/analytics", params={"name": app.seller_name})
                data = response.json()
                
                self.daily_income = str(data.get("daily", "0"))
                self.weekly_income = str(data.get("weekly", "0"))
                self.monthly_income = str(data.get("monthly", "0"))
                self.yearly_income = str(data.get("yearly", "0"))
                
                stat = data.get("stats", [])
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
            except Exception as e:
                print(f"Analytics Fetch Error: {e}")


class SellerProductCard(BoxLayout):
    p_name = StringProperty("")
    p_price = StringProperty("")
    p_desc = StringProperty("")
    p_img = StringProperty("logo.png")
    p_cat = StringProperty("")
    p_qty = StringProperty("")

    def open_edit_popup(self):
        popup = UpdateProductPopup()
        popup.p_name = self.p_name
        popup.old_name = self.p_name 
        popup.p_desc = self.p_desc
        popup.p_price = self.p_price.replace("CFA ", "") 
        popup.p_cat = self.p_cat
        popup.p_qty = self.p_qty
        popup.p_img = self.p_img
        popup.open()


# ===============================
# SELLER MANAGEMENT
# ===============================
class Seller_Manager_Page(Screen):
    def on_enter(self):
        print("sadddddddddddddddddddddddg")
        self.p_name = StringProperty("")
        self.p_price = StringProperty("")
        self.p_desc = StringProperty("")
        self.p_img = StringProperty("logo.png")
        Clock.schedule_once(lambda dt: self.load_seller_products())

    def load_seller_products(self):
        try:
            self.seller_pic = "logo.png"
            print("MMMMMMMMMMMMMMMMM")
            print(App.get_running_app().seller_name)
            
            # REQUEST REPLACING: all_product_data = manager.view_store() 
            response = requests.get(f"{BASE_URL}/seller/inventory", params={"name": App.get_running_app().seller_name})
            all_product_data = response.json() if response.status_code == 200 else []
            
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

    def update_product(self, name, des, cat, price, qty, img, Name, s_name):
        # Logic preserved: Get ID first, then update
        print(Name)
        try:
            # REQUEST REPLACING: ID = updater.get_product_id(Name)
            resp_id = requests.get(f"{BASE_URL}/product/id", params={"p_name": Name})
            ID = resp_id.json().get("id")

            # REQUEST REPLACING: updater.update_product(...)
            payload = {
                "description": des, "category": cat, "price": price, 
                "qty": qty, "img": self.img, "product_id": ID, 
                "seller_id": App.get_running_app().seller_id
            }
            requests.post(f"{BASE_URL}/product/update", json=payload)
        except Exception as e:
            print(f"Update failed: {e}")

        Clock.schedule_once(lambda dt: self.load_seller_products())



    def get_image_and_upload(self,vps_ip, seller_id, product_name):
        """
        Function Flow:
        1. Opens FileChooser.
        2. Uploads file to VPS.
        3. Returns (filename, database_path) to your main app logic.
        """
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        select_btn = Button(text="Upload Image", size_hint_y=0.15)
    
        layout.add_widget(file_chooser)
        layout.add_widget(select_btn)
    
        popup = Popup(title="Select Product Image", content=layout, size_hint=(0.9, 0.9))

        def on_upload_pressed(instance):
            if file_chooser.selection:
                self.local_full_path = file_chooser.selection[0]
                # 1. The local file name (e.g., 'camera_upload.jpg')
                self.local_filename = os.path.basename(local_full_path)
                # Start Upload to VPS
                url = f"http://{vps_ip}:8000/upload/product"
                files = {'file': (local_filename, open(local_full_path, 'rb'), 'image/jpeg')}
                data = {'seller_id': str(seller_id), 'product_name': product_name}
            
                try:
                    response = requests.post(url, files=files, data=data)
                    if response.status_code == 200:
                        # 2. The path string for the database (e.g., 'media/products/12_bread.jpg')
                        self.db_path = response.json().get("filepath")
                    
                        popup.dismiss()
                        # Return both strings back to your main UI logic
                except Exception as e:
                    print(f"Connection to VPS failed: {e}")

        select_btn.bind(on_release=on_upload_pressed)
        popup.open()
    def add_product(self, name, description, category, price, qty, img):
        # REQUEST REPLACING: adder.add_to_store(...)
        try:
            payload = {
                "seller_name": App.get_running_app().seller_name,
                "name": name, "description": description, 
                "category": category, "price": price, 
                "qty": qty, "img": self.db_path
            }
            requests.post(f"{BASE_URL}/product/add", json=payload)
        except Exception as e:
            print(f"Addition failed: {e}")
        
        Clock.schedule_once(lambda dt: self.load_seller_products())

    def delete_product(self, name):
        # REQUEST REPLACING: remover.delete_product(name)
        try:
            requests.post(f"{BASE_URL}/product/delete", json={
                "seller_name": App.get_running_app().seller_name,
                "product_name": name
            })
        except Exception as e:
            print(f"Deletion failed: {e}")
            
        Clock.schedule_once(lambda dt: self.load_seller_products())


# ===============================
# AGENT MANAGEMENT
# ===============================
class Delivery_Manager_Page(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_agents())
    
    def load_agents(self):
        try:
            # REQUEST REPLACING: all_agents = manager.view_delivery_agents()
            response = requests.get(f"{BASE_URL}/seller/agents", params={"name": App.get_running_app().seller_name})
            all_agents = response.json() if response.status_code == 200 else None
            
            if all_agents == None:
                self.ids.agent_rv.data = []
                return 0
            
            print("sadddddddddddddddddddddddg")
            print(all_agents)
            formatted = []
            for agent in all_agents:
                # REQUEST REPLACING: manager.get_a_loc(agent[1])
                loc_resp = requests.get(f"{BASE_URL}/agent/location", params={"agent_name": agent[1]})
                a_location = loc_resp.json().get("location", "Unknown")
                
                formatted.append({
                    'a_id': str(agent[0]),
                    'a_name': str(agent[1]),
                    'a_loc': str(a_location)
                }) 
            self.ids.agent_rv.data = formatted
            self.ids.agent_rv.refresh_from_data()
        except:
            print("Error loading agents")

    def add_agent(self, name, location):
        if name == "" or location == "":
            return
        try:
            # REQUEST REPLACING: adder.add_delivery_agent(name, location)
            requests.post(f"{BASE_URL}/agent/add", json={
                "seller_name": App.get_running_app().seller_name,
                "agent_name": name,
                "location": location
            })
            self.load_agents()
        except:
            print("Failed to add agent")

    def delete_agent(self, agent_id, agent_name):
        print(f"Removing Agent ID: {agent_id} ({agent_name}) from records...")
        try:
            # REQUEST REPLACING: adder.delete_delivery_agent(agent_name)
            requests.post(f"{BASE_URL}/agent/delete", json={
                "seller_name": App.get_running_app().seller_name,
                "agent_name": agent_name
            })
            self.load_agents() 
        except:
            print("Failed to delete agent")


# ===============================
# HISTORY
# ===============================

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
        Clock.schedule_once(self.load_history, 0)

    def load_history(self, dt):
        try:
            # REQUEST REPLACING: raw_data = account_manager.view_buyer_history()
            response = requests.get(f"{BASE_URL}/buyer/history", params={"name": App.get_running_app().buyer_name})
            raw_data = response.json() if response.status_code == 200 else []

            if not raw_data:
                self.ids.history_rv.data = []
                return

            self.ids.history_rv.data = [{
                "product_name": str(row[1]),
                "seller_name": str(row[2]),
                "qty": str(row[3]),
                "price": str(row[4]),
                "date": str(row[5]),
                "total_row": str(float(row[3]) * float(row[4]))
            } for row in raw_data]
        except:
            print("History load error")


class SellerHistoryPage(Screen):
    def on_enter(self):
        Clock.schedule_once(self.load_history, 0)
        print("Start\n")

    def load_history(self, dt):
        print("Start\n")
        try:
            # REQUEST REPLACING: raw_data = account_manager.view_seller_history()
            response = requests.get(f"{BASE_URL}/seller/history", params={"name": App.get_running_app().seller_name})
            raw_data = response.json() if response.status_code == 200 else []
            print("Start\n")

            if not raw_data:
                self.ids.seller_history_rv.data = []
                return
            self.ids.seller_history_rv.data = [{
                "product_name": str(row[0]),
                "qty": str(row[1]),
                "price": str(row[2]),
                "date": str(row[3]),
                "delivery_agent_name": str(row[4]),
                "total_row": str(float(row[1]) * float(row[2]))
            } for row in raw_data]
        except:
            print("Seller history load error")


# ===============================
# AGENT ORDER LOGIC
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

class Agent_Order_Page(Screen):
    def on_enter(self):
        print("**********************")
        Clock.schedule_once(lambda dt: self.load_agent_orders())

    def load_agent_orders(self):
        try:
            # REQUEST REPLACING: all_orders = manager.display_orders() 
            response = requests.get(f"{BASE_URL}/agent/orders", params={"agent_id": App.get_running_app().agent_id})
            all_orders = response.json() if response.status_code == 200 else []
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
        try:
            requests.post(f"{BASE_URL}/agent/complete_delivery", json={
                "agent_id": App.get_running_app().agent_id,
                "product_name": product_name
            })
        except:
            pass
        self.load_agent_orders()


class ConfigureBuisnessPage(Screen):
    check_text = StringProperty("")
    answer_to_password_forgotten = StringProperty("")
    text=StringProperty("C://Users//Images//logo.png")
    print("Tsuipppppppppppppp")
    new_path = StringProperty("")
    def update_profile_photo(self, vps_ip, seller_id):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        select_btn = Button(text="Set as Profile Picture", size_hint_y=0.15)
        
        layout.add_widget(file_chooser)
        layout.add_widget(select_btn)
        
        popup = Popup(title="Select Profile Photo", content=layout, size_hint=(0.9, 0.9))

        def on_upload_pressed(instance):
            if file_chooser.selection:
                full_path = file_chooser.selection[0]
                self.text=full_path
                filename = os.path.basename(full_path)
                
                url = f"http://{vps_ip}:8000/upload/profile_pic"
                
                try:
                    with open(full_path, 'rb') as f:
                        files = {'file': (filename, f, 'image/jpeg')}
                        data = {'seller_id': str(seller_id)}
                        
                        response = requests.post(url, files=files, data=data)
                        
                        if response.status_code == 200:
                            self.new_path = response.json().get("filepath")
                            # 1. Update the local class variable
                            self.seller_pic = self.new_path
                            App.get_running_app().seller_pic=self.new_path
                            # 2. Update the UI Image widget if you have one
                            self.ids.profile_image_widget.source = f"http://{vps_ip}:8000/{new_path}"
                            app
                            popup.dismiss()
                            print("Profile picture updated successfully!")
                except Exception as e:
                    print(f"Profile upload failed: {e}")

        select_btn.bind(on_release=on_upload_pressed)
        popup.open()
    def create_buiness(self):
        App.get_running_app().seller_name = "Logan"
        print("*********************************")

        b_name = self.ids.biz_name.text.strip()
        b_type = self.ids.biz_type.text.strip()
        o_time = self.ids.open_time.text.strip()
        c_time = self.ids.close_time.text.strip()
        pic = self.new_path

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

        # REQUEST REPLACING: result = self.configurer.create_entire_buisness(...)
        try:
            payload = {"seller_name": App.get_running_app().seller_name, "b_name": b_name, "b_type": b_type, "o_time": o_time, "pic": pic}
            resp = requests.post(f"{BASE_URL}/seller/configure", json=payload)
            result = resp.json().get("result")
        except:
            result = "Server connection error"

        if result == 1:
            self.check_text = "Login in............"
            App.get_running_app().Buisness_name = b_name
            App.get_running_app().Buisness_type = b_type # Corrected type in logic
            App.get_running_app().seller_opening_time = o_time
            App.get_running_app().seller_pic = pic
            self.manager.current = "seller_manager_page"
        else:
            self.check_text = str(result)


class SellerOrdersPage(Screen):
    orders_data = ListProperty([])

    def on_enter(self):
        self.fetch_seller_orders()

    def fetch_seller_orders(self):
        try:
            # REQUEST REPLACING: orders = viewer.view_orders() 
            response = requests.get(f"{BASE_URL}/seller/orders", params={"name": App.get_running_app().seller_name})
            orders = response.json() if response.status_code == 200 else []
            
            formatted_orders = []
            for row in orders:
                formatted_orders.append({
                    'order_id': str(row[0]),
                    'product_name': str(row[1]),
                    'buyer_name': str(row[3]),
                    'quantity': str(row[5]),
                    'agent_name': str(row[8]),
                    'b_location': str(row[9]),
                    'status': "PENDING"
                })
            self.orders_data = formatted_orders
        except:
            print("Failed to fetch seller orders")
    
    def manage_order(self):
        print("Opening control terminal for order:")

# ===============================
# APP
# ===============================
class GrabNGoApp(App):

    buisness_name = StringProperty()
    buisness_type = StringProperty()
    seller_location = StringProperty()
    seller_rating = NumericProperty()
    buisness_logo = StringProperty()
    seller_opening_time = StringProperty()
    seller_number_of_sales = NumericProperty()
    seller_name = StringProperty()
    seller_id = NumericProperty(0)
    seller_email = StringProperty()
    seller_phone = NumericProperty(0)
    seller_password = StringProperty()
    min_qty = NumericProperty(0)
    max_qty = NumericProperty(0)
    most_sold_product = StringProperty()
    least_sold_product = StringProperty()
    yearly_income = NumericProperty()
    monthly_income = NumericProperty()
    daily_income = NumericProperty()
    weekly_income = NumericProperty()
    seller_pic = StringProperty()
    total_sum = NumericProperty(0)
    is_active = BooleanProperty(True)
    product_bought = DictProperty({})
    order_ids = ListProperty([])

    buyer_name = StringProperty()
    buyer_id = NumericProperty(0)
    buyer_location = StringProperty()
    buyer_password = StringProperty()
    buyer_email = StringProperty()
    biz_logo = StringProperty()
    buyer_phone = NumericProperty(0)
    agent_name = StringProperty()
    agent_id = NumericProperty(0)
    agent_location = StringProperty()
    approximate_time = StringProperty()

    def build(self):
        # Using the standard ScreenManager initialization
        screenmanager = ScreenManager(transition=SlideTransition())
        
        # Adding widgets by name as defined in your code
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

        screenmanager.current = "first_page"

        return screenmanager


if __name__ == "__main__":
    GrabNGoApp().run()
