#This is Seller_Transactions (Refactored for API)
from BackEnd.Database_Manipulation_error_handling_version import *
from datetime import datetime, timedelta
import os

class Seller_View:
	def __init__(self, name):
		# No changes to logic, just internalizing connection
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.seller_name = name
		print(name)
		self.seller_id = self.getter.get_seller_id_by_name(self.seller_name)
		if self.seller_id == None:
			print("Wrong user name")

	def view_store(self):
		products = self.displayer.display_seller_product_by_seller_id(self.seller_id)
		print("***********************************")
		print(products)
		print("*********************************")
		Products = []
		for product in products:
			product = list(product)
			product[1] = self.getter.get_product_name_by_id(product[1])
			Products.append(product)
		return Products
	
	def view_orders(self):
		raw_orders = self.displayer.display_orders_by_seller_id(self.seller_id)
		processed_orders = []
		
		for order in raw_orders:
			# Convert tuple to list so it is mutable (can be changed)
			order_list = list(order)
		
			# Replace IDs with Names
			order_list[1] = self.getter.get_product_name_by_id(order_list[1])
			order_list[3] = self.getter.get_buyer_name_by_id(order_list[3])
		
			# Handle cases where agent might be None/Null
			if order_list[8]:
				order_list[8] = self.getter.get_delivery_agent_name(order_list[8])
			else:
				order_list[8] = "Unassigned"
				
			processed_orders.append(order_list)
			
		return processed_orders

	def get_a_loc(self, name):
		return self.getter.get_delivery_agent_location(name)

	def view_delivery_agents(self):
		delivery_agents = self.displayer.display_agents(self.seller_id)
		print(delivery_agents)
		print("******************************************88")
		Agents = []
		if delivery_agents == None:
			return None
		for agent in delivery_agents:
			agent = list(agent)
			agent[1] = self.getter.get_delivery_agent_name(agent[1])
			Agents.append(agent)
		return Agents

	def close_connection(self):
		self.con.close()


class Seller_Store_Manager:
	def __init__(self, name):
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.seller_name = name
		self.seller_id = self.getter.get_seller_id_by_name(name)
		self.adder = ADD_INTO_TABLES(self.con)
		self.updater = Update_Table(self.con)
		self.deleter = Delete_From_Table(self.con)

	def add_to_store(self, product_name, description, category, price, qty, img):
		product_id = self.getter.get_product_id(product_name)
		if product_id:
			db_product_qty = self.getter.get_product_qty(product_id)
			check = self.getter.get_seller_product_qty(product_id, self.seller_id)
			if check:
				print("Product already exist in store")
				return 0
			self.adder.add_into_product(product_name, qty + db_product_qty)
			self.adder.add_into_SellerProduct(self.seller_id, product_id, description, category, price, qty, img)
			self.con.commit()
			print("Product has been added to store")
		else:
			self.adder.add_into_product(product_name, qty)
			product_id = self.getter.get_product_id(product_name)
			self.adder.add_into_SellerProduct(self.seller_id, product_id, description, category, price, qty, img)			
			self.con.commit()
			print("Product has been added to store")

	def close_store(self):
		self.updater.update_seller_status(self.seller_id, "Closed")
		self.con.commit()
		print("Store has been close")

	def update_product_quantity(self, product_name, qty):
		product_id = self.getter.get_product_id(product_name)
		db_product_qty = self.getter.get_product_qty(product_id)
		db_seller_product_qty = self.getter.get_seller_product_qty(product_id, self.seller_id)
		net_qty = qty - db_seller_product_qty
		self.updater.update_seller_qty(qty, product_id, self.seller_id)
		self.updater.update_product(product_name, db_product_qty + net_qty)
		self.con.commit()
		print("Product has been updated succesfully")

	def update_product(self, des, cat, price, qty, img, ID, s_name):
		self.updater.update_entire_product(des, cat, price, qty, img, ID, s_name)
		self.con.commit()

	def update_product_description(self, name, description):
		product_id = self.getter.get_product_id(name)
		self.updater.update_product_description(self.seller_id, description, product_id)
		self.con.commit()
		print("Product description has been updated")

	def update_product_price(self, name, price):
		product_id = self.getter.get_product_id(name)
		self.updater.update_seller_product_price(self.seller_id, product_id, price)
		self.con.commit()
		print("Product price has been updated")

	def update_product_image(self, name, img):
		product_id = self.getter.get_product_id(name)
		self.updater.update_product_img(self.seller_id, img, product_id)
		self.con.commit()
		print("Product image has been updated")		

	def get_product_id(self, name):
		return self.getter.get_product_id_by_name(name)

	def delete_product(self, name):
		product_id = self.getter.get_product_id(name)
		db_product_qty = self.getter.get_product_qty(product_id)
		db_seller_product_qty = self.getter.get_seller_product_qty(product_id, self.seller_id)
		if db_seller_product_qty == None:
			print("This product do no exist in store")
			return 0
		net_qty = db_product_qty - db_seller_product_qty
		self.deleter.delete_seller_product(product_id, self.seller_id)
		self.updater.update_product(name, net_qty)
		self.con.commit()
		print("Product has been deleted succesfully")

	def _calculate_income_by_days(self, days):
		orders = self.displayer.display_seller_transactions(self.seller_id)
		total = 0
		now = datetime.now()
		if orders is None:
			return 0
		for order in orders:
			try:
				order_date = datetime.strptime(order[6], '%Y-%m-%d')
			except ValueError:
				order_date = datetime.strptime(order[6], '%d-%m-%y')
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
		history = self.displayer.display_seller_transactions(self.seller_id)
		transaction_dic = {}
		maximum_qty = 0
		if history == None:
			print("No transaction made")
			return "No transaction"

		for his in history:
			qty = his[4]
			product_name = self.getter.get_product_name_by_id(his[3])
			if product_name in transaction_dic:
				transaction_dic[product_name] += qty
			else:
				transaction_dic[product_name] = qty

		for key in transaction_dic:
			if transaction_dic[key] >= maximum_qty:
				maximum_qty = transaction_dic[key]
				maximum_prod = key
		
		minimum_qty = transaction_dic[key]
		for key in transaction_dic:
			if transaction_dic[key] <= minimum_qty:
				minimum_qty = transaction_dic[key]
				minimum_prod = key

		max_min = [maximum_prod, maximum_qty, minimum_prod, minimum_qty]
		return max_min

	def open_store(self):
		self.updater.update_seller_status(self.seller_id, "Open")
		self.con.commit()
		print("Store has been opened")

	def add_delivery_agent(self, name, location):
		agent_id = self.getter.get_delivery_agent_id(name)
		if agent_id:
			seller_deliviery_agent_id = self.getter.get_seller_delivery_agent_id(agent_id, self.seller_id)
			if seller_deliviery_agent_id == None:
				self.adder.add_into_seller_delivery_agent(agent_id, self.seller_id)
				self.con.commit()
				print("Agent has been added to store")
			else:
				print("Agent already exist in store")
		else:
			self.adder.add_into_delivery_agent(name, location)
			agent_id = self.getter.get_delivery_agent_id(name)
			self.adder.add_into_seller_delivery_agent(agent_id, self.seller_id)
			self.con.commit()
			print("Agent has been added to store")

	def delete_delivery_agent(self, name):
		agent_id = self.getter.get_delivery_agent_id(name)
		if agent_id:
			self.deleter.delete_delivery_agent(agent_id, self.seller_id)
			seller_delivery_agent_id = self.getter.get_seller_delivery_agent(agent_id)
			if seller_delivery_agent_id == None:
				self.deleter.delete_agent(agent_id)
			self.con.commit()
			print("Agent has been removed")

	def close_connection(self):
		self.con.close()


class Seller_Account_Manager(Seller_Store_Manager):
	def __init__(self, name):
		# Initializing internal connection
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.seller_name = name
		self.seller_id = self.getter.get_seller_id_by_name(name)
		self.adder = ADD_INTO_TABLES(self.con)
		self.updater = Update_Table(self.con)
		self.deleter = Delete_From_Table(self.con)

	def create_entire_buisness(self, name, type, time, pic):
		self.updater.update_entire_buisness(name, type, time, pic, self.seller_id)
		self.con.commit()
		return 1

	def change_buisness(self, name, type, location, time, pic):
		self.updater.change_entire_buisness(name, type, location, time, pic, self.seller_id)
		self.con.commit()

	def change_location(self, location):
		self.updater.update_seller_location(self.seller_id, location)
		self.con.commit()

	def change_profile_pic(self, img):
		self.updater.update_seller_profile(self.seller_id, img)
		self.con.commit()

	def change_buisness_name(self, name):
		self.updater.update_seller_name(self.seller_id, name)
		self.con.commit()

	def delete_account(self):
		ids = self.getter.get_product_id_from_seller_product_by_seller_id(self.seller_id)
		for element in ids:
			name = self.getter.get_product_name_by_id(element)
			super().delete_product(name)
		self.deleter.delete_seller_account(self.seller_id)
		self.con.commit()

	def view_seller_history(self):
		history = self.displayer.display_seller_transactions(self.seller_id)
		History = []
		if history == None:
			return 0
		for data in history:
			hist = [
				self.getter.get_product_name_by_id(data[3]),
				data[4],
				data[5],
				data[6],
				self.getter.get_delivery_agent_name(data[7])
			]
			History.append(hist)
		return History
	
	def Get_seller_info(self):
		return self.getter.get_seller_info(self.seller_id)

	def close_connection(self):
		self.con.close()

#creat a database table for delivery time

#seller1=Seller_View(con,"Tanyi Smith")
#seller1.view_delivery_agents()
#seller1.view_store()
#seller1.view_orders()
#seller2=Seller_Store_Manager(con,"Achu Bernard")
#seller2.add_delivery_agent("Jason Reed","Damas")
#seller2.delete_delivery_agent("Elena Rodriguez")
#seller2.close_store()
#seller2.add_to_store("Gel","Sold in botles","Hair product",500,55,"Gel.png")
#seller2.update_product_quantity("Douala Bread",400)
#seller2.update_product_description("Douala Bread","Very soft bread")
#seller2.update_product_price("Douala Bread","6000000")
#seller2.update_product_image("Douala Bread","Tchuuiiii.png")
#seller2.delete_product("Douala Bread")
#seller2.calculate_monthly_income()
#seller3=Seller_Account_Manager(con,"Ekani Rose")
#seller2.seller_statistics()
#seller3.change_location("Bamenda")
#seller3.change_buisness_name("Galalala")
#print(seller3.view_seller_history())
#seller3.change_opening_hours("01:00")
#seller3.delete_account()
#seller2.add_to_store("Smartphone Camon 20","Eadible","Food",780,60,"Corn.img")
con.commit()
con.close()
