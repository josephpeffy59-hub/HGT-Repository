# This is Database_Manipulation.py
import os
import sqlite3
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir,"GrabNGo_Database.db")
def Get_Database_connection():
    con= sqlite3.connect(db_path)
    return con

con=Get_Database_connection()
con.execute("PRAGMA foreign_keys = ON")


class Create_Database:
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()

            # User Table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS BUYER_ACCOUNTS(
                Buyer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Full_name TEXT NOT NULL,
                Email TEXT NOT NULL,
                Location TEXT NOT NULL,
                Phone INTEGER NOT NULL,
                Password TEXT NOT NULL NOT NULL,
                Created_at DATETIME NOT NULL,
                Status TEXT NOT NULL)
            """)

            # Seller Table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS SELLER_ACCOUNTS(
                Seller_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Full_name TEXT NOT NULL,
                Buisness_name TEXT NOT NULL,
                Buisness_type TEXT NOT NULL,
                Phone INTEGER NOT NULL,
                Email TEXT NOT NULL,
                Password TEXT NOT NULL,
                Location TEXT NOT NULL,
                Opening_time TIME NOT NULL,
                Rating REAL NOT NULL,
                Number_of_sales INTEGER NOT NULL,
                Created_at DATETIME NOT NULL,
                Profile_pic TEXT NOT NULL,
                Status TEXT NOT NULL)
            """)

            # Product table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS PRODUCT(
                Product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Product_name TEXT NOT NULL,
                Product_qty INTEGER NOT NULL)
            """)

            # Seller_Product Table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS SELLER_PRODUCT(
                Seller_ID INTEGER NOT NULL,
                Product_ID INTEGER NOT NULL,
                Description TEXT NOT NULL,
                Category TEXT NOT NULL,
                Price INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                Product_Image_path TEXT NOT NULL,
                FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID) ON DELETE CASCADE,
                FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID) ON DELETE CASCADE)
            """)

            # Orders Table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS ORDERS(
                Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Product_ID INTEGER NOT NULL,
                Seller_ID INTEGER NOT NULL,
                Buyer_ID INTEGER NOT NULL,
                Price INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                Total INTEGER NOT NULL,
                Status TEXT NOT NULL,
                Delivery_Agent_Id INTEGER,
                Buyer_Location TEXT,
                Seller_Location TEXT,
                FOREIGN KEY (Delivery_Agent_Id) REFERENCES DELIVERY_AGENT(Delivery_Agent_Id),
                FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID),
                FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID),
                FOREIGN KEY (Buyer_ID) REFERENCES BUYER_ACCOUNTS(Buyer_ID))
            """)

            # History Table
            self.cus.execute("""CREATE TABLE IF NOT EXISTS HISTORY(
                Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Buyer_ID INTEGER NOT NULL,
                Seller_ID INTEGER NOT NULL,
                Product_ID INTEGER NOT NULL,
                Product_qty INTEGER NOT NULL,
                Price INTEGER NOT NULL,
                Transaction_Date DATETIME NOT NULL,
                Delivery_Agent_Id INTEGER,
                Buyer_Location TEXT,
                Seller_Location TEXT,
                FOREIGN KEY (Delivery_Agent_Id) REFERENCES DELIVERY_AGENT(Delivery_Agent_Id),
                FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID),
                FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID),
                FOREIGN KEY (Buyer_ID) REFERENCES BUYER_ACCOUNTS(Buyer_ID))
            """)

            self.cus.execute("""CREATE TABLE IF NOT EXISTS NEIGHBORHOOD_DELIVERY (
                Route_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                City TEXT NOT NULL,
                Neighborhood_A TEXT NOT NULL,
                Neighborhood_B TEXT NOT NULL,
                Avg_Time_Minutes INTEGER NOT NULL,
                Traffic_Level TEXT NOT NULL,
                UNIQUE(City, Neighborhood_A, Neighborhood_B)
        )
    """)

            self.cus.execute("""CREATE TABLE IF NOT EXISTS DELIVERY_AGENT(
                Delivery_Agent_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Agent_Name TEXT,
                Location TEXT,
                Status TEXT)""")

            self.cus.execute("""CREATE TABLE IF NOT EXISTS SELLER_DELIVERY_AGENTS(
                Seller_Delivery_Agents_Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Delivery_Agent_Id INTEGER,
                Seller_ID INTEGER,
                Status TEXT,
                FOREIGN KEY (Delivery_Agent_Id) REFERENCES DELIVERY_AGENT(Delivery_Agent_Id),
                FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID)

                )""")

            self.connection.commit()
        except Exception as e:
            print(f"Create Table Error: {e}")

class ADD_INTO_TABLES:
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()
        except Exception as e:
            print(f"Init Error: {e}")

    def add_into_buyer_account(self, name, e_mail, location, phone, password, date_of_creation):
        try:
            self.cus.execute("""INSERT INTO BUYER_ACCOUNTS (Full_name,Email,Location,Phone,Password,Created_at,Status)
                VALUES(?,?,?,?,?,?,?)""", (name, e_mail, location, phone, password, date_of_creation, "Active"))
            self.connection.commit()
        except Exception as e:
            print(f"Add Buyer Error: {e}")
            self.connection.rollback()

    def add_into_seller_account(self, name, buisness_name, buisness_type, phone, e_mail, password, location, open_time, rating, number_of_sales, date_of_creation, img):
        try:
            self.cus.execute("""INSERT INTO SELLER_ACCOUNTS (Full_name,Buisness_name,Buisness_type,Phone,Email,Password,Location,Opening_time,Rating,Number_of_sales,Created_at,Profile_pic,Status)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (name, buisness_name, buisness_type, phone, e_mail, password, location, open_time, rating, number_of_sales, date_of_creation, img, "Active"))
            self.connection.commit()
        except Exception as e:
            print(f"Add Seller Error: {e}")
            self.connection.rollback()

    def add_into_product(self, name, qty):
        try:
            self.cus.execute("""INSERT INTO PRODUCT (Product_name,Product_qty)
                VALUES(?,?)""", (name, qty))
            self.connection.commit()
        except Exception as e:
            print(f"Add Product Error: {e}")
            self.connection.rollback()

    def add_into_Orders(self, ID1, ID2, ID3, price, qty, total,b_location,s_locaion):
        try:
            self.cus.execute("""INSERT INTO ORDERS (Product_ID,Seller_ID,Buyer_ID,Price,Quantity,Total,Status,Buyer_Location,Seller_Location)
                VALUES(?,?,?,?,?,?,?,?,?)""", (ID1, ID2, ID3, price, qty, total, "Pending",b_location,s_locaion))
            self.connection.commit()
        except Exception as e:
            print(f"Add Order Error: {e}")
            self.connection.rollback()

    def add_into_History(self, id1, id2, id3, qty, price, date, agent_id,b_location,s_locaion):
        try:
            self.cus.execute("""INSERT INTO HISTORY (Buyer_ID,Seller_ID,Product_ID,Product_qty,Price,Transaction_Date,Delivery_Agent_Id,Buyer_Location,Seller_Location)
                 VALUES(?,?,?,?,?,?,?,?,?)""", (id1, id2, id3, qty, price, date,agent_id,b_location,s_locaion))
            self.connection.commit()
        except Exception as e:
            print(f"Add History Error: {e}")
            self.connection.rollback()

    def add_into_SellerProduct(self, id1, id2, description, category, price, qty, image_path):
        try:
            self.cus.execute("""INSERT INTO SELLER_PRODUCT (Seller_ID,Product_ID,Description,Category,Price,Quantity,Product_Image_path)
                VALUES(?,?,?,?,?,?,?)""", (id1, id2, description, category, price, qty, image_path))
            self.connection.commit()
        except Exception as e:
            print(f"Add SellerProduct Error: {e}")
            self.connection.rollback()


    def add_into_delivery_agent(self,name,location):
        try:
            self.cus.execute("""INSERT INTO DELIVERY_AGENT (Agent_Name,Location,Status) 
                VALUES(?,?,?)""", (name,location,"Active"))
            self.connection.commit()
        except Exception as e:
            print(f"Add Delivery Agent Error: {e}")
            self.connection.rollback()



    def add_into_seller_delivery_agent(self,id1,id2):
        try:
            self.cus.execute("""INSERT INTO SELLER_DELIVERY_AGENTS (Delivery_Agent_Id,Seller_ID,Status) 
                VALUES(?,?,?)""", (id1,id2,"Active"))
            self.connection.commit()
        except Exception as e:
            print(f"Add Seller Deliver Agent Error: {e}")
            self.connection.rollback()


class Update_Table():
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()
        except Exception as e:
            print(f"Init Error: {e}")


    def update_delivery_agent_status(self,id1,status):
        try:
            self.cus.execute("""UPDATE DELIVERY_AGENT SET 
                Status=? WHERE
                Delivery_Agent_Id=?""", (status,id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Delivery Agent Status Error: {e}")
            self.connection.rollback()

    def update_delivery_agent(self,id1,id2):
        try:
            self.cus.execute("""UPDATE ORDERS SET 
                Delivery_Agent_Id=? WHERE
                Order_ID=?""", (id1,id2))
            self.connection.commit()
        except Exception as e:
            print(f"Update Delivery Agent Error: {e}")
            self.connection.rollback()



    def update_seller_delivery_agent_status(self,id1,id2,status):
        try:
            self.cus.execute("""UPDATE SELLER_DELIVERY_AGENTS SET 
                Status=? WHERE
                Seller_ID=? AND
                Delivery_Agent_Id=?""", (status,id1,id2))
            self.connection.commit()
        except Exception as e:
            print(f"Update Delivery Agent Etatus Error: {e}")
            self.connection.rollback()

    def update_entire_buisness(self,b_name,b_type,opening_time,pic,ID):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET 
                            Buisness_name=?,
                            Buisness_type=?,
                            Opening_time=?,
                            Profile_pic=? WHERE
                Seller_ID=?""", (b_name,b_type,opening_time,pic,ID))
            self.connection.commit()
        except Exception as e:
            print(f"Update Location Error: {e}")
            self.connection.rollback()

    def change_entire_buisness(self,b_name,b_type,location,opening_time,pic,ID):
        print("Now in database manipulation")
        print(self,b_name,b_type,location,opening_time,pic,ID)

        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET 
                            Buisness_name=?,
                            Buisness_type=?,
                            Location=?,
                            Opening_time=?,
                            Profile_pic=? WHERE
                Seller_ID=?""", (b_name,b_type,location,opening_time,pic,ID))
            self.connection.commit()
        except Exception as e:
            print(f"Update Location Error: {e}")
            self.connection.rollback()

    def update_product(self, name, qty):
        try:
            self.cus.execute("""UPDATE PRODUCT SET Product_qty=? WHERE
                Product_name=?""", (qty, name))
            self.connection.commit()
        except Exception as e:
            print(f"Update Product Error: {e}")
            self.connection.rollback()

    def update_entire_product(self,des,cat,price, qty,img,p_id,s_id):
        print("Shits about to getr real")
        print(des,cat,price, qty,img,p_id,s_id)
        try:
            self.cus.execute("""UPDATE SELLER_PRODUCT SET
                            Description=?,
                            Category=?,
                            Price=?,
                            Quantity=?,
                            Product_Image_Path=? WHERE
                Product_ID=? AND 
                Seller_ID=?""", (des,cat,price, qty,img,p_id,s_id))
            self.connection.commit()
        except Exception as e:
            print(f"Update Product Error: {e}")
            self.connection.rollback()


    def update_seller_product_price(self, id1, id2, price):
        try:
            self.cus.execute("""UPDATE SELLER_PRODUCT SET Price=? WHERE
                Product_ID=? AND Seller_ID=?""", (price, id2, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Price Error: {e}")
            self.connection.rollback()

    def update_buyer_location(self, id1, location):
        try:
            self.cus.execute("""UPDATE BUYER_ACCOUNTS SET Location=? WHERE
                Buyer_ID=?""", (location, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Location Error: {e}")
            self.connection.rollback()

    def update_seller_location(self, id1, location):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Location=? WHERE
                Seller_ID=?""", (location, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Location Error: {e}")
            self.connection.rollback()

    def update_seller_rating(self, id1, rating):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Rating=? WHERE
                Seller_ID=?""", (rating, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Rating Error: {e}")
            self.connection.rollback()

    def update_seller_number_of_sales(self, id1, number_of_sales):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Number_of_sales=? WHERE
                Seller_ID=?""", (number_of_sales, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Sales Error: {e}")
            self.connection.rollback()

    def update_seller_qty(self, qty, id1, id2):
        try:
            self.cus.execute("""UPDATE SELLER_PRODUCT SET Quantity=? WHERE
                Product_ID=? AND
                Seller_ID=?""", (qty, id1, id2))
            self.connection.commit()
        except Exception as e:
            print(f"Update Qty Error: {e}")
            self.connection.rollback()

    def update_order_qty(self, ID, qty):
        try:
            self.cus.execute("""UPDATE ORDERS SET Quantity=? WHERE
                Order_ID=?""", (qty, ID))
            self.connection.commit()
        except Exception as e:
            print(f"Update Order Qty Error: {e}")
            self.connection.rollback()

    def update_seller_status(self, seller_id, status):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Status=?
                WHERE Seller_ID=?""", (status, seller_id))
            self.connection.commit()
            print(seller_id)
        except Exception as e:
            print(f"Update Status Error: {e}")
            self.connection.rollback()

    def update_product_description(self, seller_id, description, product_id):
        try:
            self.cus.execute("""UPDATE SELLER_PRODUCT SET Description=? WHERE
                Seller_ID=? AND
                Product_ID=?""", (description, seller_id, product_id))
            self.connection.commit()
        except Exception as e:
            print(f"Update Desc Error: {e}")
            self.connection.rollback()

    def update_product_img(self, seller_id, img, product_id):
        try:
            self.cus.execute("""UPDATE SELLER_PRODUCT SET Product_Image_path=?
                WHERE Seller_ID=? AND
                Product_ID=?""", (img, seller_id, product_id))
            self.connection.commit()
        except Exception as e:
            print(f"Update Img Error: {e}")
            self.connection.rollback()

    def update_seller_profile(self, id, img):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Profile_pic=? WHERE
                Seller_ID=?""", (img, id))
            self.connection.commit()
        except Exception as e:
            print(f"Update Profile Error: {e}")
            self.connection.rollback()

    def update_seller_name(self, id1, name):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Buisness_name=? WHERE
                Seller_ID=?""", (name, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Name Error: {e}")
            self.connection.rollback()

    def update_seller_opening_time(self, id1, time):
        try:
            self.cus.execute("""UPDATE SELLER_ACCOUNTS SET Opening_time=?
                WHERE Seller_ID=?""", (time, id1))
            self.connection.commit()
        except Exception as e:
            print(f"Update Time Error: {e}")
            self.connection.rollback()

    def update_order_status(self,ID):
        try:
            self.cus.execute("""UPDATE ORDERS SET
                Status=? WHERE
                Order_ID=?""", ("Done", ID))
            self.connection.commit()
        except Exception as e:
            print(f"Update Order Qty Error: {e}")
            self.connection.rollback()


class Delete_From_Table:
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()
        except Exception as e:
            print(f"Init Error: {e}")

    def delete_seller_product(self, id1, id2):
        try:
            self.cus.execute("""DELETE FROM SELLER_PRODUCT WHERE
                Product_ID = ? AND Seller_ID =?""", (id1, id2))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Error: {e}")
            self.connection.rollback()

    def delete_delivery_agent(self, id1, id2):
        try:
            self.cus.execute("""DELETE FROM SELLER_DELIVERY_AGENTS WHERE
                Delivery_Agent_Id = ? AND
                Seller_ID =?""", (id1, id2))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Error: {e}")
            self.connection.rollback()


    def delete_agent(self, id1):
        try:
            self.cus.execute("""DELETE FROM DELIVERY_AGENT WHERE
                Delivery_Agent_Id = ?""", (id1,))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Error: {e}")
            self.connection.rollback()



    def delete_order(self, id1):
        try:
            self.cus.execute("""DELETE FROM ORDERS WHERE Order_ID = ?""", (id1,))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Order Error: {e}")
            self.connection.rollback()

    def delete_buyer_account(self, id1):
        try:
            self.cus.execute("""DELETE FROM BUYER_ACCOUNTS WHERE
                Buyer_ID = ?""", (id1,))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Buyer Error: {e}")
            self.connection.rollback()

    def delete_seller_account(self, id1):
        try:
            self.cus.execute("""DELETE FROM SELLER_ACCOUNTS WHERE Seller_ID = ?""", (id1,))
            self.connection.commit()
        except Exception as e:
            print(f"Delete Seller Error: {e}")
            self.connection.rollback()

class Get_From_Tables:
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()
        except Exception as e:
            print(f"Init Error: {e}")

    def get_buyer_id_by_name(self, name):
        try:
            self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
                Full_name =? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None
    def get_sellers(self):
        try:
            self.cus.execute("""SELECT * FROM SELLER_ACCOUNTS""")
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_buyer_id_by_password(self, password):
        try:
            self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
                Password =? """, (password,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_id_by_password(self, password):
        try:
            self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
                Password =? """, (password,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_free_agent(self,id1):
        print("Now we bout to get a free delivery agent")
        print(id1)
        try:
            self.cus.execute("""SELECT Delivery_Agent_Id FROM SELLER_DELIVERY_AGENTS WHERE
                Seller_ID =? """, (id1,))
            Data = self.cus.fetchall()
            print("sadgdf")
            data=[]
            data = [row[0] for row in Data]
            print(data)
            if data:
                for seller_id in data:
                    self.cus.execute("""SELECT Agent_Name FROM DELIVERY_AGENT WHERE
                        Delivery_Agent_Id =? AND
                        Status="Active" """, (seller_id,))

                name=self.cus.fetchone()
                print("This is the free agent gotten")
                print(name)
                return name

            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_buyer_info(self, ID):
        try:
            self.cus.execute("""SELECT * FROM BUYER_ACCOUNTS WHERE
                Buyer_ID =? """, (ID,))
            data = self.cus.fetchall()
            if data:
#                buyer_ids = [row[0] for row in data]
                return data
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_info(self, ID):
        try:
            self.cus.execute("""SELECT * FROM SELLER_ACCOUNTS WHERE
                Seller_ID =? """, (ID,))
            data = self.cus.fetchall()
            if data:
#                buyer_ids = [row[0] for row in data]
                return data
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_buyer_id_by_location(self, location):
        try:
            self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
                Location =? """, (location,))
            data = self.cus.fetchall()
            if data:
                buyer_ids = [row[0] for row in data]
                return buyer_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_buyer_id_by_email(self, email):
        try:
            self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE Email=? """, (email,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None
    def get_buyer_name_by_id(self,ID):
        try:
            self.cus.execute("""SELECT Full_Name FROM BUYER_ACCOUNTS WHERE Buyer_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_id_by_location(self, location):
        try:
            self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
                Location =? """, (location,))
            data = self.cus.fetchall()
            if data:
                seller_ids = [row[0] for row in data]
                return seller_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_id_by_email(self, email):
        try:
            self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
                Email=? """, (email,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_status(self, seller_id):
        try:
            self.cus.execute("""SELECT Status FROM SELLER_ACCOUNTS WHERE
                Seller_ID=? """, (seller_id,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_id_by_name(self, name):
        try:
            self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
                Full_name =? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_rating(self, ID):
        try:
            self.cus.execute("""SELECT Rating FROM SELLER_ACCOUNTS WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_number_of_sales(self, ID):
        try:
            self.cus.execute("""SELECT Number_of_sales FROM SELLER_ACCOUNTS WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_name_by_id(self, ID):
        try:
            self.cus.execute("""SELECT Buisness_name FROM SELLER_ACCOUNTS WHERE
                Seller_ID =? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_location(self, name):
        try:
            self.cus.execute("""SELECT Location FROM SELLER_ACCOUNTS WHERE
                Full_name =? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None



    def get_seller_name_by_buisness_name(self, name):
        try:
            self.cus.execute("""SELECT Full_name FROM SELLER_ACCOUNTS WHERE
                Buisness_name=? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_product_id_by_name(self, name):
        try:
            self.cus.execute("""SELECT Product_ID FROM PRODUCT WHERE
                Product_name =? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_product_name_by_id(self, ID):
        try:
            self.cus.execute("""SELECT Product_name FROM PRODUCT WHERE
                Product_ID =? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_product_id(self, name):
        try:
            self.cus.execute("""SELECT Product_ID FROM PRODUCT WHERE
                Product_name =? """, (name,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_delivery_agent_name(self,id1):
        try:
            self.cus.execute("""SELECT Agent_Name FROM DELIVERY_AGENT WHERE
                Delivery_Agent_Id =? """, (id1,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_delivery_agent_id(self,name):
        try:
            self.cus.execute("""SELECT Delivery_Agent_Id FROM DELIVERY_AGENT WHERE
                Agent_Name =? """, (name,))
            data = self.cus.fetchone()
            print(data)
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_delivery_agent_location(self,name):
        print("111111111111111111111111111")
        print(name)
        try:
            self.cus.execute("""SELECT Location FROM DELIVERY_AGENT WHERE
                Agent_Name =? """, (name,))
            data = self.cus.fetchone()
            print(data)
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_seller_delivery_agent_id(self,id1,id2):
        try:
            self.cus.execute("""SELECT Seller_Delivery_Agents_Id FROM SELLER_DELIVERY_AGENTS WHERE
                Delivery_Agent_Id =? AND
                Seller_ID = ?""", (id1,id2))
            data = self.cus.fetchone()
            print(data)
            print("sadf")
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_seller_delivery_agent(self,id1):
        try:
            self.cus.execute("""SELECT Seller_Delivery_Agents_Id FROM SELLER_DELIVERY_AGENTS WHERE
                Delivery_Agent_Id =? """, (id1,))
            data = self.cus.fetchone()
            print(data)
            print("sadf")
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_unit_time(self,location1,location2):
        try:
            self.cus.execute("""SELECT Avg_Time_Minutes FROM NEIGHBORHOOD_DELIVERY WHERE
            Neighborhood_A =? AND
            Neighborhood_B=? OR
            Neighborhood_A=? AND 
            Neighborhood_B=?""", (location1,location2,location2,location1))
            data = self.cus.fetchone()
            print(data)
            print("sadf")
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_seller_id_from_seller_product_by_product_id(self, id1):
        try:
            self.cus.execute("""SELECT Seller_ID FROM SELLER_PRODUCT WHERE
                Product_ID =? """, (id1,))
            data = self.cus.fetchall()
            if data:
                seller_ids = [row[0] for row in data]
                return seller_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_product_id_from_seller_product_by_seller_id(self, id1):
        try:
            self.cus.execute("""SELECT Product_ID FROM SELLER_PRODUCT
                WHERE Seller_ID =? """, (id1,))
            data = self.cus.fetchall()
            if data:
                product_ids = [row[0] for row in data]
                return product_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_seller_product_qty(self, ID, seller_id):
        try:
            self.cus.execute("""SELECT Quantity FROM SELLER_PRODUCT WHERE
                Product_ID =? AND
                Seller_ID=? """, (ID, seller_id))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_order_id_by_seller_id(self, ID):
        try:
            self.cus.execute("""SELECT Order_ID FROM ORDERS WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                order_ids = [row[0] for row in data]
                return order_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_agent_daily_work(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                order_ids = [row[0] for row in data]
                return order_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None



    def get_order_id_by_product_id(self, ID):
        try:
            self.cus.execute("""SELECT Order_ID FROM ORDERS WHERE
                Product_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                order_ids = [row[0] for row in data]
                return order_ids
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_seller_id_from_order_id(self, ID):
        try:
            self.cus.execute("""SELECT Seller_ID FROM ORDERS WHERE
                Order_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                data=data[0]
                return data
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None


    def get_agent_id_from_order_id(self, ID):
        try:
            self.cus.execute("""SELECT Delivery_Agent_Id FROM ORDERS WHERE
                Order_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                data=data[0]
                return data
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

    def get_product_qty(self, ID):
        try:
            self.cus.execute("""SELECT Product_qty FROM PRODUCT WHERE
                Product_ID=? """, (ID,))
            data = self.cus.fetchone()
            if data:
                return data[0]
            else:
                return None
        except Exception as e:
            print(f"Get Error: {e}")
            return None

class Display_From_Table:
    def __init__(self, conn):
        try:
            self.connection = conn
            self.cus = self.connection.cursor()
        except Exception as e:
            print(f"Init Error: {e}")

    def display_seller_product_by_product_id(self, ID):
        try:
            self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
                Product_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_product_details_by_product_id_and_seller_id(self, ID1, ID2):
        print("And now \n\n THis is the final boss")
        print(ID1,ID2)
        try:
            self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
                Product_ID=? AND
                Seller_ID=?""", (ID1, ID2))
            data = self.cus.fetchall()
            products = []
            for row in data:
                product = [row[2], row[3], row[4], row[5], row[6]]
                products.append(product)
            if data:
                return products
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_seller_product_by_seller_id(self, ID):
        try:
            self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_seller_product_by_seller_id_and_category(self, ID, category):
        try:
            self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
                Seller_ID=? AND
                Category=? """, (ID, category))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_orders_by_seller_id(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_orders_by_product_id(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Product_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_order(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Order_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None


    def display_agents(self,id1):
        try:
            self.cus.execute("""SELECT * FROM SELLER_DELIVERY_AGENTS WHERE
                Seller_ID=? """, (id1,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None



    def display_orders_by_buyer_id(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Buyer_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None

    def display_history(self, ID):
        try:
            self.cus.execute("""SELECT * FROM HISTORY WHERE
                Buyer_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None


    def display_delivery_agent_history(self, ID):
        try:
            self.cus.execute("""SELECT * FROM HISTORY WHERE
                Delivery_Agent_Id=ID? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None


    def display_delivery_agent_orders(self, ID):
        try:
            self.cus.execute("""SELECT * FROM ORDERS WHERE
                Delivery_Agent_Id= ? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None


    def display_seller_transactions(self, ID):
        try:
            self.cus.execute("""SELECT * FROM HISTORY WHERE
                Seller_ID=? """, (ID,))
            data = self.cus.fetchall()
            if data:
                return data
            else:
                return None
        except Exception as e:
            print(f"Display Error: {e}")
            return None
        
# Final Execution
try:
    data = Create_Database(con)
#    data2 = ADD_INTO_TABLES(con)
    con.commit()
except Exception as e:
    print(f"Main Loop Error: {e}")
finally:
    if 'con' in locals():
        con.close()
