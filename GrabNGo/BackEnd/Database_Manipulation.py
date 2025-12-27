#This is Database_Manipulation.py
import sqlite3

con= sqlite3.connect("GrabNGo_Database.db")
con.execute("PRAGMA foreign_keys = ON")
class Create_Database:
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()

#       User Table
		self.cus.execute("""CREATE TABLE IF NOT EXISTS BUYER_ACCOUNTS(
			Buyer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Full_name TEXT,
			Email TEXT,
			Location TEXT,
			Phone INTEGER,
			Password TEXT,
			Created_at DATETIME,
			Status TEXT)

		""")

#       Seller Table
		self.cus.execute("""CREATE TABLE IF NOT EXISTS SELLER_ACCOUNTS(
			Seller_ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Full_name TEXT,
			Buisness_name TEXT,
			Buisness_type TEXT,
			Phone INTEGER,
			Email TEXT,
			Password TEXT,
			Location TEXT,
			Opening_time TIME,
			Rating REAL,
			Number_of_sales INTEGER,
			Created_at DATETIME,
			Profile_pic TEXT,
			Status TEXT)

		""")



#       Product table
		self.cus.execute("""CREATE TABLE IF NOT EXISTS PRODUCT(
			Product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Product_name TEXT,
			Product_qty INTEGER)
		""")



#       Seller_Product Table
		self.cus.execute("""CREATE TABLE IF NOT EXISTS SELLER_PRODUCT(
			Seller_ID INTEGER,
			Product_ID INTEGER,
			Description TEXT,
			Category TEXT,
			Price INTEGER,
			Quantity INTEGER,
			Product_Image_path TEXT,

			FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID) ON DELETE CASCADE,
			FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID) ON DELETE CASCADE)
		""")



#       Orders Table
		self.cus.execute("""CREATE TABLE IF NOT EXISTS ORDERS(
			Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Product_ID INTEGER,
			Seller_ID INTEGER,
			Buyer_ID INTEGER,
			Price INTEGER,
			Quantity INTEGER,
			Total INTEGER,
			Status TEXT,

			FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID),
			FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID),
			FOREIGN KEY (Buyer_ID) REFERENCES BUYER_ACCOUNTS(Buyer_ID))

		""")


#       History Table

		self.cus.execute("""CREATE TABLE IF NOT EXISTS HISTORY(
			Transaction_ID INTEGER PRIMARY KEY AUTOINCREMENT,
			Buyer_ID INTEGER,
			Seller_ID INTEGER,
			Product_ID INTEGER,
			Product_qty INTEGER,
			Price INTEGER,
			Transaction_Date DATETIME,
			FOREIGN KEY (Product_ID) REFERENCES PRODUCT(Product_ID),
			FOREIGN KEY (Seller_ID) REFERENCES SELLER_ACCOUNTS(Seller_ID),
			FOREIGN KEY (Buyer_ID) REFERENCES BUYER_ACCOUNTS(Buyer_ID))

		""")



class ADD_INTO_TABLES:
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()

	def add_into_buyer_account(self,name,e_mail,location,phone,password,date_of_creation):
		self.cus.execute("""INSERT INTO BUYER_ACCOUNTS (Full_name,Email,Location,Phone,Password,Created_at,Status)
			VALUES(?,?,?,?,?,?,?)""",(name,e_mail,location,phone,password,date_of_creation,"Active"))
		self.connection.commit()

	def add_into_seller_account(self,name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation,img):
		self.cus.execute("""INSERT INTO SELLER_ACCOUNTS (Full_name,Buisness_name,Buisness_type,Phone,Email,Password,Location,Opening_time,Rating,Number_of_sales,Created_at,Profile_pic,Status)
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",(name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation,img,"Active"))
		self.connection.commit()


	def add_into_product(self,name,qty):
		self.cus.execute("""INSERT INTO PRODUCT (Product_name,Product_qty)
			VALUES(?,?)""",(name,qty))
		self.connection.commit()


	def add_into_Orders(self,ID1,ID2,ID3,price,qty,total):
		self.cus.execute("""INSERT INTO ORDERS (Product_ID,Seller_ID,Buyer_ID,Price,Quantity,Total,Status)
			VALUES(?,?,?,?,?,?,?)""",(ID1,ID2,ID3,price,qty,total,"Pending"))
		self.connection.commit()



	def add_into_History(self,id1,id2,id3,qty,price,date):
		self.cus.execute("""INSERT INTO HISTORY (Buyer_ID,Seller_ID,Product_ID,Product_qty,Price,Transaction_Date)
			 VALUES(?,?,?,?,?,?)""",(id1,id2,id3,qty,price,date))
		self.connection.commit()


	def add_into_SellerProduct(self,id1,id2,description,category,price,qty,image_path):
		self.cus.execute("""INSERT INTO SELLER_PRODUCT (Seller_ID,Product_ID,Description,Category,Price,Quantity,Product_Image_path)
			VALUES(?,?,?,?,?,?,?)""",(id1,id2,description,category,price,qty,image_path))
		self.connection.commit()




class Update_Table():
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()

	def update_product(self,name,qty):
		self.cus.execute("""UPDATE PRODUCT SET
			Product_qty=?
			WHERE Product_name=?""",(qty,name))

		self.connection.commit()


	def update_seller_product_price(self,id1,id2,price):
		self.cus.execute("""UPDATE SELLER_PRODUCT SET
			Price=?
			WHERE Product_ID=? AND
			Seller_ID=?""",(price,id2,id1))

		self.connection.commit()



	def update_buyer_location(self,id1,location):
		self.cus.execute("""UPDATE BUYER_ACCOUNTS SET
			Location=?
			WHERE Buyer_ID=?""",(location,id1))

		self.connection.commit()



	def update_seller_location(self,id1,location):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Location=?
			WHERE Seller_ID=?""",(location,id1))

		self.connection.commit()

	def update_seller_rating(self,id1,rating):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Rating=?
			WHERE Seller_ID=?""",(rating,id1))

		self.connection.commit()

	def update_seller_number_of_sales(self,id1,number_of_sales):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Number_of_sales=?
			WHERE Seller_ID=?""",(number_of_sales,id1))

		self.connection.commit()


	def update_seller_qty(self,qty,id1,id2):
		self.cus.execute("""UPDATE SELLER_PRODUCT SET
			Quantity=?
			WHERE Product_ID=? AND
			Seller_ID=?""",(qty,id1,id2))

		self.connection.commit()


	def update_order_qty(self,ID,qty):
		self.cus.execute("""UPDATE ORDERS SET
			Quantity=?
			WHERE Order_ID=?""",(qty,ID))

		self.connection.commit()


	def update_seller_status(self,seller_id,status):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Status=?
			WHERE Seller_ID=?""",(status,id1))

		self.connection.commit()


	def update_product_description(self,seller_id,description,product_id):
		self.cus.execute("""UPDATE SELLER_PRODUCT SET
			Description=?
			WHERE Seller_ID=? AND
			Product_ID=?""",(description,seller_id,product_id))

		self.connection.commit()

	def update_product_img(self,seller_id,img,product_id):
		self.cus.execute("""UPDATE SELLER_PRODUCT SET
			Product_Image_path=?
			WHERE Seller_ID=? AND
			Product_ID=?""",(img,seller_id,product_id))

		self.connection.commit()



	def update_seller_profile(self,id,img):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Profile_pic=?
			WHERE Seller_ID=?""",(img,id1))

		self.connection.commit()


	def update_seller_name(self,id1,name):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Buisness_name=?
			WHERE Seller_ID=?""",(name,id1))

		self.connection.commit()

	def update_seller_opening_time(self,id1,time):
		self.cus.execute("""UPDATE SELLER_ACCOUNTS SET
			Opening_time=?
			WHERE Seller_ID=?""",(time,id1))

		self.connection.commit()




class Delete_From_Table:
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()

	def delete_seller_product(self,id1,id2):
		self.cus.execute("""DELETE FROM SELLER_PRODUCT
			WHERE Product_ID = ? AND
			Seller_ID =?
			""", (id1,id2))
		self.connection.commit()


	def delete_order(self,id1):
		self.cus.execute("""DELETE FROM ORDERS
			WHERE Order_ID = ?
			""", (id1,))

		self.connection.commit()

	def delete_buyer_account(self,id1):
		self.cus.execute("""DELETE FROM BUYER_ACCOUNTS
			WHERE Buyer_ID = ?
			""", (id1,))

		self.connection.commit()

	def delete_seller_account(self,id1):
		self.cus.execute("""DELETE FROM SELLER_ACCOUNTS
			WHERE Seller_ID = ?
			""", (id1,))

		self.connection.commit()


class Get_From_Tables:
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()

	def get_buyer_id_by_name(self,name):
		self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
			Full_name =? """,(name,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None

	def get_buyer_id_by_location(self,location):
		self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
			Location =? """,(location,))
		data= self.cus.fetchall()
		if data:
			buyer_ids=[row[0] for row in data]
			return buyer_ids

		else:
			return None

	def get_buyer_id_by_email(self,email):
		self.cus.execute("""SELECT Buyer_ID FROM BUYER_ACCOUNTS WHERE
			Email=? """,(email,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None
		

	def get_seller_id_by_location(self,location):
		self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
			Location =? """,(location,))
		data= self.cus.fetchall()
		if data:
			seller_ids=[row[0] for row in data]
			return seller_ids

		else:
			return None

	def get_seller_id_by_email(self,email):
		self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
			Email=? """,(email,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None
		
	def get_seller_status(self,seller_id):
		self.cus.execute("""SELECT Status FROM SELLER_ACCOUNTS WHERE
			Seller_ID=? """,(seller_id,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None


	def get_seller_id_by_name(self,name):
		self.cus.execute("""SELECT Seller_ID FROM SELLER_ACCOUNTS WHERE
			Full_name =? """,(name,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None


	def get_seller_rating(self,ID):
		self.cus.execute("""SELECT Rating FROM SELLER_ACCOUNTS WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None



	def get_seller_number_of_sales(self,ID):
		self.cus.execute("""SELECT Number_of_sales FROM SELLER_ACCOUNTS WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None


	def get_seller_name_by_id(self,ID):
		self.cus.execute("""SELECT Buisness_name FROM SELLER_ACCOUNTS WHERE
			Seller_ID =? """,(ID,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None



	def get_product_id_by_name(self,name):
		self.cus.execute("""SELECT Product_ID FROM PRODUCT WHERE
			Product_name =? """,(name,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None

	def get_product_name_by_id(self,ID):
		self.cus.execute("""SELECT Product_name FROM PRODUCT WHERE
			Product_ID =? """,(ID,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None




	def get_product_id(self,name):
		self.cus.execute("""SELECT Product_ID FROM PRODUCT WHERE
			Product_name =? """,(name,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None


	def get_seller_id_from_seller_product_by_product_id(self,id1):
		self.cus.execute("""SELECT Seller_ID FROM SELLER_PRODUCT WHERE
			Product_ID =? """,(id1,))
		data= self.cus.fetchall()
		if data:
			seller_ids = [row[0] for row in data]
			return seller_ids

		else:
			return None



	def get_product_id_from_seller_product_by_seller_id(self,id1):
		self.cus.execute("""SELECT Product_ID FROM SELLER_PRODUCT WHERE
			Seller_ID =? """,(id1,))
		data= self.cus.fetchall()
		if data:
			product_ids = [row[0] for row in data]
			print(product_ids)
			return product_ids

		else:
			return None
		


	def get_seller_product_qty(self,ID,seller_id):
		self.cus.execute("""SELECT Quantity FROM SELLER_PRODUCT WHERE
			Product_ID =? AND
			Seller_ID=? """,(ID,seller_id))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None



	def get_order_id_by_seller_id(self,ID):
		self.cus.execute("""SELECT Order_ID FROM ORDERS WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			order_ids = [row[0] for row in data]
			return order_ids

		else:
			return None

	def get_order_id_by_product_id(self,ID):
		self.cus.execute("""SELECT Order_ID FROM ORDERS WHERE
			Product_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			order_ids = [row[0] for row in data]
			return order_ids

		else:
			return None


	def get_product_qty(self,ID):
		self.cus.execute("""SELECT Product_qty FROM PRODUCT WHERE
			Product_ID=? """,(ID,))
		data= self.cus.fetchone()
		if data:
			return data[0]

		else:
			return None


class Display_From_Table:
	def __init__(self,conn):
		self.connection=conn
		self.cus=self.connection.cursor()


	def display_seller_product_by_product_id(self,ID):
		self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
			Product_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data
		else:
			return None



	def display_product_details_by_product_id_and_seller_id(self,ID1,ID2):
		self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
			Product_ID=? AND
			Seller_ID=?""",(ID1,ID2,))
		data= self.cus.fetchall()
		products=[]
		for row in data:
			product=[]
			product.append(row[2])
			product.append(row[3])
			product.append(row[4])
			product.append(row[5])
			product.append(row[6])
			products.append(product)

		if data:
			return products
		else:
			return None


	def display_seller_product_by_seller_id(self,ID):
		self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None

	def display_seller_product_by_seller_id_and_category(self,ID,category):
		self.cus.execute("""SELECT * FROM SELLER_PRODUCT WHERE
			Seller_ID=? AND
			Category=? """,(ID,category,))
		data= self.cus.fetchall()
		if data:

			return data

		else:
			return None



	def display_orders_by_seller_id(self,ID):
		self.cus.execute("""SELECT * FROM ORDERS WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None



	def display_orders_by_product_id(self,ID):
		self.cus.execute("""SELECT * FROM ORDERS WHERE
			Product_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None


	def display_order(self,ID):
		self.cus.execute("""SELECT * FROM ORDERS WHERE
			Order_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None



	def display_orders_by_buyer_id(self,ID):
		self.cus.execute("""SELECT * FROM ORDERS WHERE
			Buyer_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None


	def display_history(self,ID):
		self.cus.execute("""SELECT * FROM HISTORY WHERE
			Buyer_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None


	def display_seller_transactions(self,ID):
		self.cus.execute("""SELECT * FROM HISTORY WHERE
			Seller_ID=? """,(ID,))
		data= self.cus.fetchall()
		if data:
			return data

		else:
			return None




data=Create_Database(con)
#data2=ADD_INTO_TABLES(con)
#data2.add_into_buyer_account("Corn","yo@gmail.com","Yaounde",677334989,"shuijj@hggh","21-12-3")

#data2.add_into_Orders(2,3,6,400,34,455)
#data2.add_into_History(1,9,1,566,555,"12-23-23")
#data2.add_into_product("Vegetables",1700)
#data2.add_into_SellerProduct(12,12,"GIII","guii",600,788,"sdfsadf")
#data3=Update_Table()
#data3.update_product("Gas",555)
#data3.update_buyer_location(1,"Nyom")
#data3.update_seller_location(1,"Koletam")
#data4=Delete_From_Table()
#data4.delete_order(1)
#data4.delete_seller_product(5)
#data5=Get_From_Tables(con)
#data5.get_product_id_from_seller_product_by_seller_id(2)
#print("dsafaaaaaasdfaaaaaaaaaaa")
#print(data5.get_buyer_id_by_email("yo@gmai"))
#print("dsafaaaaaasdfaaaaaaaaaaa")
#data6=Display_From_Table(con)
#print(data6.display_seller_product_by_seller_id_and_category(12,"guii"))
#data6.display_history(4)

con.commit()
con.close()
