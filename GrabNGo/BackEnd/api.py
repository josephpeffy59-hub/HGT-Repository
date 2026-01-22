from fastapi import FastAPI, Body, HTTPException
from typing import Optional
import uvicorn
import os
import re
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles



# IMPORTING YOUR UNMODIFIED LOGIC
# This assumes buyer_login.py is in the same folder on your VPS
from buyer_login import Buyer_Login 
from seller_login import Seller_Login 
from buyer_transactions import (
    Buyer_Search_Transactions, 
    Buyer_Visit_Seller, 
    Buyer_Cart_Manager,
    Buyer_Account_Manager,
    Buyer_Payment_Transactions,
    Buyer_Submit_Review
)
from seller_transactions import (
    Seller_View,
    Seller_Store_Manager,
    Seller_Account_Manager
)
app = FastAPI(title="Market App API")

@app.get("/")
def read_root():
    return {"status": "Server is running"}

# ==========================================
# BUYER LOGIN / SIGNUP ENDPOINTS
# ==========================================
@app.get("/buyer/id")
async def get_buyer_id_endpoint(name: str):
    """
    Returns buyer ID by buyer name
    Safe for frontend usage
    """
    manager = Buyer_Login()
    try:
        buyer_id = manager.get_buyer_id(name)

        if buyer_id is None:
            raise HTTPException(
                status_code=404,
                detail="Buyer not found"
            )

        return {
            "status": 1,
            "buyer_id": buyer_id
        }

    finally:
        manager.close_connection()

@app.post("/buyer/create")
async def signup(data: dict = Body(...)):
    """
    Kivy calls this for: create_buyer_account
    Expected JSON: {name, email, location, phone, password, date}
    """
    manager = Buyer_Login()
    try:
        result = manager.create_buyer_account(
            data['name'], 
            data['email'], 
            data['location'], 
            data['phone'], 
            data['password'], 
            data['date']
        )
        return {"result": result}
    finally:
        manager.close_connection()

@app.post("/buyer/login")
async def login(data: dict = Body(...)):
    manager = Buyer_Login()
    try:
        result = manager.login(
            data['name'],
            data['email'],
            data['password']
        )

        if result == 1:
            info = manager.Get_buyer_info(data['name'])
            return {
                "result": 1,
                "info": info
            }
        else:
            raise HTTPException(status_code=401, detail=result)

    finally:
        manager.close_connection()

# IMPORTING YOUR UNMODIFIED LOGIC
# Ensure seller_login.py is in the same directory on your VPS

# ==========================================
# SELLER LOGIN / SIGNUP ENDPOINTS
# ==========================================
@app.get("/validate/email")
def validate_email(email: str):
    return {"valid": Buyer_Login().validate_email(email)}

@app.get("/validate/password")
def validate_password(password: str):
    return {"valid": Buyer_Login().validate_password(password)}


@app.get("/seller/id")
async def get_seller_id_endpoint(name: str):
    """
    Returns seller ID by seller name
    """
    manager = Seller_Login()
    try:
        seller_id = manager.get_seller_id(name)

        if seller_id is None:
            raise HTTPException(
                status_code=404,
                detail="Seller not found"
            )

        return {
            "status": 1,
            "seller_id": seller_id
        }

    finally:
        manager.close_connection()

@app.post("/seller/create")
async def seller_signup(data: dict = Body(...)):
    """
    Kivy calls this for: create_seller_account
    Expected JSON: {name, biz_name, biz_type, phone, email, password, location, open_time, rating, sales, date, img}
    """
    manager = Seller_Login()
    try:
        result = manager.create_seller_account(
            data['name'],
            data['buisness_name'],
            data['buisness_type'],
            data['phone'],
            data['e_mail'],
            data['password'],
            data['location'],
            data['open_time'],
            data['rating'],
            data['number_of_sales'],
            data['date_of_creation'],
            data['img']
        )
        return {"result": result}
    finally:
        manager.close_connection()
@app.post("/seller/login")
async def seller_login_endpoint(data: dict = Body(...)):
    manager = Seller_Login()
    try:
        result = manager.login(
            data['name'],
            data['email'],
            data['password']
        )

        if result == 1:
            info = manager.Get_seller_info(data['name'])
            return {
                "result": 1,
                "info": info
            }
        else:
            raise HTTPException(status_code=401, detail=result)

    finally:
        manager.close_connection()

@app.get("/seller/info")
async def get_seller_info_endpoint(name: str):
    """
    Kivy calls this for: Get_seller_info
    Expects name as a URL parameter: ?name=BusinessName
    """
    manager = Seller_Login()
    try:
        info = manager.Get_seller_info(name)
        # Returns the list of lists exactly as your Kivy code expects
        return info 
    finally:
        manager.close_connection()
@app.post("/agent/login")
async def agent_login(data: dict = Body(...)):
    manager = Delivery_Agent_Login()
    try:
        success = manager.login(data["name"], data["id"])
        return {"success": bool(success)}
    finally:
        manager.close_connection()


# IMPORTING YOUR TRANSACTION CLASSES

# ==========================================
# STORE & PRODUCT BROWSING
# ==========================================

@app.get("/seller/id")
async def get_seller_id(name: str):
    manager = Buyer_Search_Transactions(name="System")
    try:
        s_id = manager.getter.get_seller_id_by_name(name)
        return {"id": s_id}
    finally:
        manager.close_connection()

@app.get("/sellers")
async def get_all_sellers():
    """Matches Kivy: requests.get(f"{BASE_URL}/sellers")"""
    manager = Buyer_Search_Transactions(name="System") # Name not critical for global list
    try:
        sellers = manager.Get_sellers()
        return sellers
    finally:
        manager.close_connection()

@app.get("/products")
async def get_seller_products(seller_name: str):
    """Matches Kivy: requests.get(f"{BASE_URL}/products", params={"seller_name": ...})"""
    manager = Buyer_Visit_Seller(name="System")
    try:
        products = manager.visit_sellers(seller_name)
        return products
    finally:
        manager.close_connection()

@app.get("/product/detail")
async def get_product_detail_endpoint(p_name: str, s_name: str):
    """Matches Kivy: requests.get(f"{BASE_URL}/product/detail", ...)"""
    manager = Buyer_Search_Transactions(name="System")
    try:
        details = manager.get_product_detail(p_name, s_name)
        return details
    finally:
        manager.close_connection()

# ==========================================
# CART MANAGEMENT
# ==========================================

@app.post("/order/place")
async def place_order_endpoint(data: dict = Body(...)):
    """Matches Kivy: requests.post(f"{BASE_URL}/order/place", json=payload)"""
    manager = Buyer_Cart_Manager(data['buyer_name'], data['buyer_location'])
    try:
        manager.place_order(data['product_name'], data['seller_name'], data['quantity'])
        return {"status": "success"}
    finally:
        manager.close_connection()

@app.get("/cart")
async def view_cart_endpoint(buyer_name: str, location: str = "Default"):
    """Matches Kivy: requests.get(f"{BASE_URL}/cart", params=params)"""
    manager = Buyer_Cart_Manager(buyer_name, location)
    try:
        cart_data = manager.view_cart()
        return cart_data
    finally:
        manager.close_connection()

@app.post("/cart/update")
async def update_cart_qty(data: dict = Body(...)):
    manager = Buyer_Cart_Manager(data['buyer_name'], data['location'])
    try:
        manager.update_buyer_product_qty(data['order_id'], data['qty'])
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/cart/delete")
async def delete_cart_item(data: dict = Body(...)):
    manager = Buyer_Cart_Manager(data['buyer_name'], data['location'])
    try:
        manager.delete_from_cart(data['order_id'])
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/cart/clear")
async def clear_cart_endpoint(data: dict = Body(...)):
    manager = Buyer_Cart_Manager(data['buyer_name'], "System")
    try:
        manager.empty_cart()
        return {"status": 1}
    finally:
        manager.close_connection()

# ==========================================
# PAYMENT & INVENTORY
# ==========================================

@app.post("/inventory/reduce")
async def reduce_inventory(data: dict = Body(...)):
    """Matches Kivy: requests.post(f"{BASE_URL}/inventory/reduce", json=payload)"""
    # Location not needed for stock reduction
    manager = Buyer_Payment_Transactions("System", "System") 
    try:
        manager.reduce_stock_of_purchase_items(data['product'], data['seller'], data['qty'])
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/delivery/assign")
async def assign_agent(data: dict = Body(...)):
    manager = Buyer_Payment_Transactions("System", "System")
    try:
        agent = manager.asign_delivery_agent(data['seller_name'], data['order_id'])
        return {"agent_name": agent}
    finally:
        manager.close_connection()

# ==========================================
# REVIEWS & FINALIZATION
# ==========================================

@app.post("/order/finalize")
async def finalize_order(data: dict = Body(...)):
    """Matches Kivy: requests.post(f"{BASE_URL}/order/finalize", ...)"""
    manager = Buyer_Submit_Review("System")
    try:
        manager.insert_into_history(data['order_id'], data['date'])
        manager.delete_from_orders(data['order_id'])
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/seller/rate")
async def rate_seller(data: dict = Body(...)):
    manager = Buyer_Submit_Review("System")
    try:
        manager.update_rating(data['seller_id'], data['rating'])
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/delivery/populate")
async def populate_delivery_agent(data: dict = Body(...)):
    manager = Buyer_Payment_Transactions("System", "System")
    try:
        manager.populate_delivery_agent(
            order_id=data["order_id"],
            agent_name=data["agent_name"]
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.get("/delivery/time")
async def get_delivery_time(location: str):
    manager = Buyer_Payment_Transactions("System", "System")
    try:
        time = manager.get_delivery_time(location)

        if time is None:
            return {"time": "0"}   # IMPORTANT: never return None

        return {"time": time}
    finally:
        manager.close_connection()


# IMPORTING YOUR SELLER CLASSES
from seller_transactions import (
    Seller_View,
    Seller_Store_Manager,
    Seller_Account_Manager
)

# ==========================================
# SELLER STORE & INVENTORY
# ==========================================

@app.get("/seller/store")
async def view_seller_store(seller_name: str):
    """Matches: manager.view_store()"""
    manager = Seller_View(seller_name)
    try:
        return manager.view_store()
    finally:
        manager.close_connection()

@app.post("/seller/product/add")
async def add_product_to_store(data: dict = Body(...)):
    """Matches: manager.add_to_store(...)"""
    manager = Seller_Store_Manager(data['seller_name'])
    try:
        manager.add_to_store(
            data['p_name'], data['p_desc'], data['p_cat'], 
            data['p_price'], data['p_qty'], data['p_img']
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/seller/product/update")
async def update_product_details(data: dict = Body(...)):
    """Matches: manager.update_product(...)"""
    manager = Seller_Store_Manager(data['seller_name'])
    try:
        manager.update_product(
            data['des'], data['cat'], data['price'], 
            data['qty'], data['img'], data['id'], data['s_name']
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/seller/product/delete")
async def delete_product_from_store(data: dict = Body(...)):
    manager = Seller_Store_Manager(data['seller_name'])
    try:
        manager.delete_product(data['p_name'])
        return {"status": 1}
    finally:
        manager.close_connection()

# ==========================================
# BUSINESS ANALYTICS (INCOME)
# ==========================================

@app.get("/seller/stats/income")
async def get_seller_income(seller_name: str, period: str):
    """
    period can be: 'daily', 'weekly', 'monthly', 'yearly'
    """
    manager = Seller_Store_Manager(seller_name)
    try:
        if period == "daily": return {"income": manager.calculate_daily_income()}
        if period == "weekly": return {"income": manager.calculate_weekly_income()}
        if period == "monthly": return {"income": manager.calculate_monthly_income()}
        if period == "yearly": return {"income": manager.calculate_yearly_income()}
    finally:
        manager.close_connection()

@app.get("/seller/stats/products")
async def get_seller_product_stats(seller_name: str):
    """Returns max/min sold products"""
    manager = Seller_Store_Manager(seller_name)
    try:
        return {"stats": manager.seller_statistics()}
    finally:
        manager.close_connection()



# ===============================
# BUYER PROFILE API
# ===============================
@app.get("/buyer/info")
async def get_buyer_info(name: str):
    manager = Buyer_Login()
    try:
        info = manager.Get_buyer_info(name)
        return info  # returns list of lists, matching Kivy logic
    finally:
        manager.close_connection()

@app.post("/buyer/update_location")
async def update_buyer_location(data: dict = Body(...)):
    manager = Buyer_Login()
    try:
        buyer_id = manager.get_buyer_id(data['name'])
        manager.account_adder.update_buyer_location(buyer_id, data['location'])
        manager.con.commit()
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/buyer/delete")
async def delete_buyer_account(data: dict = Body(...)):
    manager = Buyer_Login()
    try:
        buyer_id = manager.get_buyer_id(data['name'])
        manager.account_adder.delete_buyer_account(buyer_id)
        manager.con.commit()
        return {"status": 1}
    finally:
        manager.close_connection()

# ===============================
# SELLER PROFILE API
# ===============================
@app.get("/seller/info")
async def get_seller_info(name: str):
    manager = Seller_Login()
    try:
        info = manager.Get_seller_info(name)
        return info  # returns list of lists
    finally:
        manager.close_connection()

@app.post("/seller/update_profile")
async def update_seller_profile(data: dict = Body(...)):
    manager = Seller_Login()
    try:
        seller_id = manager.get_seller_id(data['current_name'])
        manager.account_adder.update_seller_profile(
            seller_id,
            data['biz_name'],
            data['biz_type'],
            data['location'],
            data['time'],
            data['pic']
        )
        manager.con.commit()
        return {"status": 1}
    finally:
        manager.close_connection()

# ===============================
# SELLER ANALYTICS API
# ===============================
@app.get("/seller/analytics")
async def get_seller_analytics(name: str):
    manager = Seller_Store_Manager(name)
    try:
        income_data = {
            "daily": manager.calculate_daily_income(),
            "weekly": manager.calculate_weekly_income(),
            "monthly": manager.calculate_monthly_income(),
            "yearly": manager.calculate_yearly_income()
        }
        stats = manager.seller_statistics()  # returns [most_sold, max_qty, least_sold, min_qty]
        return {"daily": income_data["daily"], "weekly": income_data["weekly"],
                "monthly": income_data["monthly"], "yearly": income_data["yearly"],
                "stats": stats}
    finally:
        manager.close_connection()

# ==========================================
# SELLER ACCOUNT & AGENTS
# ==========================================

@app.get("/seller/info")
async def get_seller_profile_info(name: str):
    """Matches Kivy: requests.get(f"{BASE_URL}/seller/info", params={"name": app.seller_name})"""
    manager = Seller_Account_Manager(name)
    try:
        return manager.Get_seller_info()
    finally:
        manager.close_connection()

@app.post("/seller/update_business")
async def update_business_info(data: dict = Body(...)):
    """Matches: manager.change_buisness(...)"""
    manager = Seller_Account_Manager(data['seller_name'])
    try:
        manager.change_buisness(
            data['name'], data['type'], data['location'], 
            data['time'], data['pic']
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/seller/agent/add")
async def add_agent_endpoint(data: dict = Body(...)):
    manager = Seller_Store_Manager(data['seller_name'])
    try:
        manager.add_delivery_agent(data['agent_name'], data['location'])
        return {"status": 1}
    finally:
        manager.close_connection()



# Configuration for your Contabo VPS storage
MEDIA_DIR = "media"
PRODUCT_DIR = os.path.join(MEDIA_DIR, "products")

# Create folders if they don't exist
os.makedirs(PRODUCT_DIR, exist_ok=True)

# Mount the folder so the Buyer App can see the images later
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

@app.post("/upload/product")
async def upload_product_image(
    file: UploadFile = File(...), 
    seller_id: str = Form(...), 
    product_name: str = Form(...)
):
    """
    This endpoint receives the file from your Kivy 'on_upload_pressed' function.
    It saves it and returns the path that you then pass to your 'add_product' class.
    """
    try:
        # 1. Clean up the filename
        extension = os.path.splitext(file.filename)[1]
        clean_name = product_name.replace(" ", "_").lower()
        filename = f"{seller_id}_{clean_name}{extension}"
        
        # 2. Define the path where it lives on the VPS
        save_path = os.path.join(PRODUCT_DIR, filename)
        
        # 3. Define the string you will save in your SQLite DB
        db_path_string = f"media/products/{filename}"

        # 4. Save the binary data to disk
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 5. Return the string back to Kivy
        return {"filepath": db_path_string}

    except Exception as e:
        print(f"Upload Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during upload")


# Configuration for Profile Pictures
PROFILE_DIR = os.path.join("media", "profiles")
os.makedirs(PROFILE_DIR, exist_ok=True)

@app.post("/upload/profile_pic")
async def upload_profile_pic(
    file: UploadFile = File(...), 
    seller_id: str = Form(...)
):
    """
    Saves a profile picture. Naming it by seller_id ensures 
    that the old one is overwritten when a new one is uploaded.
    """
    try:
        # 1. Get extension (e.g., .jpg)
        extension = os.path.splitext(file.filename)[1]
        
        # 2. Filename is just the seller ID (e.g., "123.jpg")
        filename = f"{seller_id}{extension}"
        save_path = os.path.join(PROFILE_DIR, filename)
        
        # 3. Path to store in your 'Sellers' table in SQLite
        db_path_string = f"media/profiles/{filename}"

        # 4. Save to VPS disk
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"filepath": db_path_string}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile upload failed: {e}")

@app.get("/product/id")
async def get_product_id(p_name: str):
    manager = Seller_Store_Manager("System")  # or use seller context if needed
    try:
        return {"id": manager.get_product_id(p_name)}
    finally:
        manager.close_connection()

@app.post("/product/update")
async def update_product_endpoint(data: dict = Body(...)):
    manager = Seller_Store_Manager("System")
    try:
        manager.update_product(
            data["product_id"], data["description"], data["category"], 
            data["price"], data["qty"], data["img"], data["seller_id"]
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.post("/product/add")
async def add_product_endpoint(data: dict = Body(...)):
    manager = Seller_Store_Manager(data["seller_name"])
    try:
        manager.add_to_store(
            data["name"], data["description"], data["category"], 
            data["price"], data["qty"], data["img"]
        )
        return {"status": 1}
    finally:
        manager.close_connection()

@app.get("/seller/agents")
async def get_seller_agents(name: str):
    manager = Seller_Store_Manager(name)
    try:
        return manager.view_delivery_agents()
    finally:
        manager.close_connection()

@app.get("/agent/location")
async def get_agent_location(agent_name: str):
    manager = Seller_Store_Manager("System")
    try:
        return {"location": manager.get_a_loc(agent_name)}
    finally:
        manager.close_connection()

@app.get("/buyer/history")
async def get_buyer_history(name: str):
    manager = Buyer_Account_Manager(name)
    try:
        return manager.view_buyer_history()
    finally:
        manager.close_connection()

@app.get("/seller/history")
async def get_seller_history(name: str):
    manager = Seller_Store_Manager(name)
    try:
        return manager.view_seller_history()
    finally:
        manager.close_connection()

@app.get("/agent/orders")
async def get_agent_orders(agent_id: str):
    manager = Delivery_Manager(agent_id)
    try:
        return manager.display_orders()
    finally:
        manager.close_connection()

@app.post("/agent/complete_delivery")
async def complete_delivery_endpoint(data: dict = Body(...)):
    manager = Delivery_Manager(data["agent_id"])
    try:
        manager.complete_delivery(data["product_name"])
        return {"status": 1}
    finally:
        manager.close_connection()
@app.post("/seller/configure")
async def configure_business(data: dict = Body(...)):
    manager = Seller_Account_Manager(data["seller_name"])
    try:
        manager.create_entire_business(
            data["b_name"], data["b_type"], data["o_time"], data["c_time"], data["pic"]
        )
        return {"result": 1}
    finally:
        manager.close_connection()

@app.get("/seller/orders")
async def get_seller_orders(name: str):
    manager = Seller_Store_Manager(name)
    try:
        return manager.view_orders()
    finally:
        manager.close_connection()
