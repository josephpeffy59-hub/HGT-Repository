from BackEnd.Database_Manipulation_error_handling_version import *
import os
import sqlite3

class Buyer_Search_Transactions:
	def __init__(self, name):
		# Initialize connection internally
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.buyer_name = name
		self.buyer_id = self.getter.get_buyer_id_by_name(name)

	def check_seller_status(self, seller_id):
		status = self.getter.get_seller_status(seller_id)
		if status == "Open" or status == "Active":
			print("Store is open")
			return 1
		elif status == "Closed":
			print("Store is Closed")
			return 0
		elif status == "Banned":
			print("Seller Account has been banned")
			return 0

	def get_seller_by_location(self, location):
		ids = self.getter.get_seller_id_by_location(location)
		sellers = []
		if ids == None:
			print("No store found")
			return 0
		for s_id in ids:
			if self.displayer.display_seller_product_by_seller_id(s_id) != None:
				if self.check_seller_status(s_id):
					sellers.append(self.displayer.display_seller_product_by_seller_id(s_id))
			else:
				print("Stores found with no product in them")
				sellers.append(self.getter.get_seller_name_by_id(s_id))
		return sellers

	def Search_seller(self, name):
		seller_id = self.getter.get_seller_id_by_name(name)
		seller = None
		if self.check_seller_status(seller_id):
			seller = self.displayer.display_seller_product_by_seller_id(seller_id)
		return seller

	def search_product_in_store_by_category(self, category, store_name):
		seller_id = self.getter.get_seller_id_by_name(store_name)
		if self.check_seller_status(seller_id):
			products = self.displayer.display_seller_product_by_seller_id_and_category(seller_id, category)
			return products

	def search_product(self, name): 
		product_id = self.getter.get_product_id(name)
		product = self.displayer.display_seller_product_by_product_id(product_id)
		return product

	def get_product_detail(self, product_name, seller_name):
		seller_id = self.getter.get_seller_id_by_name(seller_name)
		if self.check_seller_status(seller_id):
			product_id = self.getter.get_product_id(product_name)
			details = self.displayer.display_product_details_by_product_id_and_seller_id(product_id, seller_id)
			return details
		
	def Get_sellers(self):
		return self.getter.get_sellers()

	def find_seller_id(self, name):
		return self.getter.get_seller_id_by_name(name)
	
	def close_connection(self):
		self.con.close()


class Buyer_Visit_Seller(Buyer_Search_Transactions):
	def __init__(self, name):
		# No con passed here, parent __init__ handles it
		super().__init__(name)

	def Get_seller_name(self, name):
		return self.getter.get_seller_name_by_buisness_name(name)

	def visit_sellers(self, name):
		seller_id = self.getter.get_seller_id_by_name(name)
		if super().check_seller_status(seller_id):
			products = self.displayer.display_seller_product_by_seller_id(seller_id)
			Products = []
			for product in products:
				product = list(product)
				product[1] = self.getter.get_product_name_by_id(product[1])
				Products.append(product)
			return Products


class Buyer_Cart_Manager(Buyer_Search_Transactions):
	def __init__(self, name, location):
		super().__init__(name)
		self.adder = ADD_INTO_TABLES(self.con)
		self.deleter = Delete_From_Table(self.con)
		self.updater = Update_Table(self.con)
		self.Location = location

	def place_order(self, product_name, seller_name, quantity):
		seller_id = self.getter.get_seller_id_by_name(seller_name)
		seller_location = self.getter.get_seller_location(seller_name)
		if super().check_seller_status(seller_id):
			product_id = self.getter.get_product_id(product_name)
			product_quantity = self.getter.get_seller_product_qty(product_id, seller_id)
			if product_quantity >= quantity:
				details = self.displayer.display_product_details_by_product_id_and_seller_id(product_id, seller_id)
				price = details[0][2]
				self.adder.add_into_Orders(ID1=product_id, ID2=seller_id, ID3=self.buyer_id, price=price, qty=quantity, total=quantity*price, b_location=self.Location, s_locaion=seller_location)
				self.con.commit()
				print("Order has been placed")
			else:
				print("Limited stock")
				return None

	def update_buyer_product_qty(self, ID, qty):
		self.updater.update_order_qty(ID, qty)
		self.con.commit()

	def view_cart(self):
		dailly_Cart = self.displayer.display_orders_by_buyer_id(self.buyer_id)
		Cart = []
		if dailly_Cart == None:
			return None
		for product in dailly_Cart:
			if product[7] == "Pending":
				cart = [
					product[0],
					self.getter.get_product_name_by_id(product[1]),
					self.getter.get_seller_name_by_id(product[2]),
					product[4],
					product[5],
					product[6]
				]
				Cart.append(cart)
		return Cart

	def delete_from_cart(self, ID):
		self.deleter.delete_order(ID)
		self.con.commit()
		print("Order deleted")

	def compute_sum(self):
		cart_items = self.view_cart()
		total = 0
		if cart_items:
			for product in cart_items:
				total += product[5]
		return total

	def empty_cart(self):
		dailly_Cart = self.displayer.display_orders_by_buyer_id(self.buyer_id)
		for product in dailly_Cart:
			if product[7] == "Pending":
				self.deleter.delete_order(product[0])
		self.con.commit()
		print("Cart has been emptied")

	def change_quantity(self, Id, qty):
		self.updater.update_order_qty(Id, qty)
		self.con.commit()


class Buyer_Account_Manager:
	def __init__(self, name):
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.buyer_name = name
		self.buyer_id = self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter = Delete_From_Table(self.con)
		self.updater = Update_Table(self.con)
		
	def get_buyer_info(self):
		return self.getter.get_buyer_info(self.buyer_id)

	def change_location(self, location):
		self.updater.update_buyer_location(self.buyer_id, location)
		self.con.commit()

	def view_buyer_history(self):
		history = self.displayer.display_history(self.buyer_id)
		History = []
		if history == None:
			return 0
		for data in history:
			hist = [
				self.getter.get_buyer_name_by_id(data[1]),
				self.getter.get_product_name_by_id(data[3]),
				self.getter.get_seller_name_by_id(data[2]),
				data[4],
				data[5],
				data[6]
			]
			History.append(hist)
		return History

	def delete_account(self):
		self.deleter.delete_buyer_account(self.buyer_id)
		self.con.commit()

	def close_connection(self):
		self.con.close()


class Buyer_Payment_Transactions:
	def __init__(self, name, location):
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.buyer_name = name
		self.buyer_id = self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter = Delete_From_Table(self.con)
		self.updater = Update_Table(self.con)
		self.location = location

	def reduce_stock_of_purchase_items(self, product_name, seller_name, quantity_sold):
		product_id = self.getter.get_product_id(product_name)
		seller_id = self.getter.get_seller_id_by_name(seller_name)
		current_qty = self.getter.get_seller_product_qty(product_id, seller_id)
		all_product_qty = self.getter.get_product_qty(product_id)
		self.updater.update_seller_qty(current_qty - quantity_sold, product_id, seller_id)
		self.updater.update_product(product_name, all_product_qty - quantity_sold)
		self.con.commit()

	def asign_delivery_agent(self, name, order_id):
		seller_id = self.getter.get_seller_id_by_name(name)
		agent = self.getter.get_free_agent(seller_id)
		if agent:
			agent_id = self.getter.get_delivery_agent_id(name)
			self.updater.update_delivery_agent(agent_id, order_id)
			self.updater.update_seller_delivery_agent_status(seller_id, agent_id, "Delivering")
			self.con.commit()
		return agent

	def get_delivery_time(self, location1):
		time = self.getter.get_unit_time(self.location, location1)
		if time == None:
			return "Contact Seller To get Approximated Deliver Time"
		return time
		
	def close_connection(self):
		self.con.close()


class Buyer_Submit_Review:
	def __init__(self, name):
		self.con = Get_Database_connection()
		self.getter = Get_From_Tables(self.con)
		self.displayer = Display_From_Table(self.con)
		self.adder = ADD_INTO_TABLES(self.con)
		self.buyer_name = name
		self.buyer_id = self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter = Delete_From_Table(self.con)
		self.updater = Update_Table(self.con)

	def insert_into_history(self, order_id, date):
		order = self.displayer.display_order(order_id)
		if order == None:
			return 0
		order = order[0]
		self.adder.add_into_History(order[3], order[2], order[1], order[5], order[4], date, order[8], order[9], order[10])
		self.updater.update_seller_delivery_agent_status("Active", order[2], order[8])
		self.con.commit()

	def update_rating(self, seller_id, buyer_rating):
		rating = self.getter.get_seller_rating(seller_id)
		number_of_sales = self.getter.get_seller_number_of_sales(seller_id)
		new_rating = float((number_of_sales * rating) + buyer_rating) / (number_of_sales + 1)
		self.updater.update_seller_number_of_sales(seller_id, number_of_sales + 1)
		self.updater.update_seller_rating(seller_id, new_rating)
		self.con.commit()

	def delete_from_orders(self, order_id):
		self.deleter.delete_order(order_id)
		self.updater.update_order_status(order_id)
		self.con.commit()
	
	def close_connection(self):
		self.con.close()
