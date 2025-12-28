from Database_Manipulation import *
from datetime import datetime, timedelta
con= sqlite3.connect("GrabNGo_Database.db")
class Seller_View:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.seller_name=name
		self.seller_id=self.getter.get_seller_id_by_name(name)


	def view_store(self):
		product=self.displayer.display_seller_product_by_seller_id(self.seller_id)
		print(product)
		return product


	def view_orders(self):
		orders=self.displayer.display_orders_by_seller_id(self.seller_id)
		print(orders)
		return orders


class Seller_Store_Manager:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.seller_name=name
		self.seller_id=self.getter.get_seller_id_by_name(name)
		self.adder=ADD_INTO_TABLES(con)
		self.updater=Update_Table(con)
		self.deleter=Delete_From_Table(con)		


	def add_to_store(self,product_name,description,category,price,qty,img):
		product_id=self.getter.get_product_id(product_name)
		if product_id:
			db_product_qty=self.getter.get_product_qty(product_id)
			check=self.getter.get_seller_product_qty(product_id,self.seller_id)
			if check:
				print("Product already exist in store")
				return 0
			self.adder.add_into_product(product_name,qty+db_product_qty)
			self.adder.add_into_SellerProduct(self.seller_id,product_id,description,category,price,qty,img)
			print("Product has been added to store")

		else:
			self.adder.add_into_product(product_name,qty)
			product_id=self.getter.get_product_id(product_name)
			self.adder.add_into_SellerProduct(self.seller_id,product_id,description,category,price,qty,img)			
			print("Product has been added to store")


	def close_store(self):
		self.updater.update_seller_status(self.seller_id,"Closed")
		print("Store has been close")


	def update_product_quantity(self,product_name,qty):
		product_id=self.getter.get_product_id(product_name)
		db_product_qty=self.getter.get_product_qty(product_id)
		db_seller_product_qty=self.getter.get_seller_product_qty(product_id,self.seller_id)
		net_qty=qty-db_seller_product_qty
		self.updater.update_seller_qty(qty,product_id,self.seller_id)
		self.updater.update_product(product_name,db_product_qty+net_qty)
		print("Product has been updated succesfully")


	def update_product_description(self,name,description):
		product_id=self.getter.get_product_id(name)
		self.updater.update_product_description(self.seller_id,description,product_id)
		print("Product description has been updated")

	def update_product_price(self,name,price):
		product_id=self.getter.get_product_id(name)
		self.updater.update_seller_product_price(self.seller_id,product_id,price)
		print("Product price has been updated")
		


	def update_product_image(self,name,img):
		product_id=self.getter.get_product_id(name)
		self.updater.update_product_img(self.seller_id,img,product_id)
		print("Product image has been updated")		


	def delete_product(self,name):
		product_id=self.getter.get_product_id(name)
		db_product_qty=self.getter.get_product_qty(product_id)
		db_seller_product_qty=self.getter.get_seller_product_qty(product_id,self.seller_id)
		print(db_product_qty)
		print(db_seller_product_qty)
		print(self.seller_id)
		print(product_id)
		net_qty=db_product_qty-db_seller_product_qty
		self.deleter.delete_seller_product(product_id,self.seller_id)
		self.updater.update_product(name,net_qty)
		print("Product has been deleted succesfully")
		

	def _calculate_income_by_days(self, days):
		orders = self.displayer.display_seller_transactions(self.seller_id)
		total = 0
		now = datetime.now()

		for order in orders:
			order_date = datetime.strptime(order[6], '%Y-%m-%d')
			if now - order_date <= timedelta(days=days):
				total += (order[4] * order[5])

		return total

	def calculate_daily_income(self):
		income = self._calculate_income_by_days(1)
		print(f"Daily Income: {income}")
		return income


	def calculate_weekly_income(self):
		income = self._calculate_income_by_days(7)
		print(f"Weekly Income: {income}")
		return income



	def calculate_monthly_income(self):
		income = self._calculate_income_by_days(30)
		print(f"Monthly Income: {income}")
		return income


	def calculate_yearly_income(self):
		income = self._calculate_income_by_days(365)
		print(f"Yearly Income: {income}")
		return income


	def seller_statistics(self):
		history=self.displayer.display_seller_transactions(self.seller_id)
		transaction_dic={}
		maximum_qty=0
		for his in history:
			qty=his[4]
			product_name=self.getter.get_product_name_by_id(his[3])
			if product_name in transaction_dic:
				transaction_dic[product_name]+=qty
			else:
				transaction_dic[product_name]=qty

		for key in transaction_dic:
			if transaction_dic[key]>=maximum_qty:
				maximum_qty=transaction_dic[key]
				maximum_prod=key
		
		minimum_qty=transaction_dic[key]

		for key in transaction_dic:
			if transaction_dic[key]<=minimum_qty:
				minimum_qty=transaction_dic[key]
				minimum_prod=key


		print(f"Maximum quantity:   {maximum_qty}")
		print(f"Product with maximum quantity:    {maximum_prod}")
		print(f"Minimum quantity:    {minimum_qty}")
		print(f"Product with minimum quantity:   {minimum_prod}")
		max_min=[]
		max_min.append(maximum_prod)
		max_min.append(maximum_qty)
		max_min.append(minimum_prod)
		max_min.append(minimum_qty)
		return max_min


	def open_store(self):
		self.updater.update_seller_status(self.seller_id,"Open")
		print("Store has been close")


class Seller_Account_Manager(Seller_Store_Manager):
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.seller_name=name
		self.seller_id=self.getter.get_seller_id_by_name(name)
		self.adder=ADD_INTO_TABLES(con)
		self.updater=Update_Table(con)
		self.deleter=Delete_From_Table(con)		



	def change_location(self,location):
		self.updater.update_seller_location(self.seller_id,location)
		print("User location has been updated")


	def change_profile_pic(self,img):
		self.updater.update_seller_profile(self.seller_id,img)
		print("User profile has been updated")		


	def change_buisness_name(self,name):
		self.updater.update_seller_name(self.seller_id,name)
		print("Seller name has been updated succesfully")


	def delete_account(self):
		ids=self.getter.get_product_id_from_seller_product_by_seller_id(self.seller_id)
		print(ids)
		for element in ids:
			name=self.getter.get_product_name_by_id(element)
			super().delete_product(name)

		self.deleter.delete_seller_account(self.seller_id)
		print("Account has been deleted succesfully")



	def view_seller_history(self):
		history=self.displayer.display_seller_transactions(self.seller_id)
		return history

	def change_opening_hours(self,time):
		self.updater.update_seller_opening_time(self.seller_id,time)
		print("Opening time has  been updated succesfully")



#creat a database table for delivery time

seller1=Seller_View(con,"Fosso Kamga")
#seller1.view_store()
#seller1.view_orders()
seller2=Seller_Store_Manager(con,"Tchakounte Paul")
#seller2.update_product_quantity("Palm Oil 5L",400)
#seller2.update_product_description("Rice 25kg Neima","Very bad rice")
#seller2.update_product_price("Office Paper A4","6000000")
#seller2.update_product_image("Office Paper A4","Tchuuiiii.png")
#seller2.delete_product("Office Paper A4")
#seller2.calculate_monthly_income()
seller3=Seller_Account_Manager(con,"Brenda Bi")
#seller2.seller_statistics()
#seller3.change_location("Bamenda")
#seller3.change_buisness_name("Galalala")
#print(seller3.view_seller_history())
#seller3.change_opening_hours("01:00")
seller3.delete_account()
#seller2.add_to_store("Smartphone Camon 20","Eadible","Food",780,60,"Corn.img")
con.commit()
con.close()