from Database_Manipulation import *
con= sqlite3.connect("GrabNGo_Database.db")
class Buyer_Search_Transactions:
	def __init__(self,conn,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(name)


	def check_seller_status(self,seller_id):
		status=self.getter.get_seller_status(seller_id)
		if status=="Open":
			print("Store is open")
			return 1
		elif status == "Closed":
			print("Store is Closed")
			return 0

		elif status == "Banned":
			print("Seller Account has been banned")
			return 0

	def get_seller_by_location(self,location):
		ids=self.getter.get_seller_id_by_location(location)
		sellers=[]
		for s_id in ids:

			if self.displayer.display_seller_product_by_seller_id(s_id) != None:
				sellers.append(self.displayer.display_seller_product_by_seller_id(s_id))

		return sellers


	def Search_seller(self,name):
		seller_id=self.getter.get_seller_id_by_name(name)
		seller=self.displayer.display_seller_product_by_seller_id(seller_id)
		return seller

	def search_product_in_store_by_category(self,category,store_name):
		seller_id=self.getter.get_seller_id_by_name(store_name)
		products=self.displayer.display_seller_product_by_seller_id_and_category(seller_id,category)
		return products

	def search_product(self,name): 
		product_id=self.getter.get_product_id(name)
		product=self.displayer.display_seller_product_by_product_id(product_id)
		return product


	def get_product_detail(self,product_name,seller_name):
		seller_id=self.getter.get_seller_id_by_name(seller_name)
		product_id=self.getter.get_product_id(product_name)
		details=self.displayer.display_product_details_by_product_id_and_seller_id(product_id,seller_id)
		return details



class Buyer_Visit_Seller:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(self.buyer_name)


	def visit_seller(self,name):
		seller_id=self.getter.get_seller_id_by_name(name)
		products=self.displayer.display_seller_product_by_seller_id(seller_id)
		return products



class Buyer_Cart_Manager:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.adder=ADD_INTO_TABLES(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter=Delete_From_Table(con)
		self.updater=Update_Table(con)

	def place_order(self,product_name,seller_name,quantity): # check if qty is sufficient don't reduce qyt from PRODUCT and PRODUCT_SELLER then  create the array
		seller_id=self.getter.get_seller_id_by_name(seller_name)
		product_id=self.getter.get_product_id(product_name)
		product_quantity=self.getter.get_seller_product_qty(product_id,seller_id)
		if product_quantity>=quantity:
			details=self.displayer.display_product_details_by_product_id_and_seller_id(product_id,seller_id)
			print(details)
			price=details[0][2]
			self.adder.add_into_Orders(ID1=product_id,ID2=seller_id,ID3=self.buyer_id,price=price,qty=quantity,total=quantity*price)
			print("Order has been placed")

		else:
			print("Limited stock")
			return None


	def view_cart(self):
		dailly_Cart=self.displayer.display_orders_by_buyer_id(self.buyer_id)
		print(dailly_Cart)
		print("yhdfffffffffffff")
		Cart=[]
		cart=[]
		for product in dailly_Cart:
			if product[7]=="Pending":
				cart=[]
				cart.append(product[0])
				cart.append(self.getter.get_product_name_by_id(product[1]))
				cart.append(self.getter.get_seller_name_by_id(product[2]))
				cart.append(product[4])
				cart.append(product[5])
				cart.append(product[6])
				Cart.append(cart)

		return Cart



	def delete_from_cart(self,ID):
		self.deleter.delete_order(ID)
		print("Order deleted")

	def compute_sum(self):
		dailly_Cart=self.displayer.display_orders_by_buyer_id(self.buyer_id)
		Cart=[]
		cart=[]
		for product in dailly_Cart:
			if product[7]=="Pending":
				cart=[]
				cart.append(product[0])
				cart.append(self.getter.get_product_name_by_id(product[1]))
				cart.append(self.getter.get_seller_name_by_id(product[2]))
				cart.append(product[4])
				cart.append(product[5])
				cart.append(product[6])
				Cart.append(cart)
		total=0
		for product in Cart:
			print(product)
			total+=product[5]

		print(total)
		return total




	def empty_cart(self):
		dailly_Cart=self.displayer.display_orders_by_buyer_id(self.buyer_id)
		for product in dailly_Cart:
			if product[7]=="Pending":
				self.deleter.delete_order(product[0])


		print("Cart has been emptied")
		


	def change_quantity(self,Id,qty):# To change the quantity of a purchased item
		self.updater.update_order_qty(Id,qty)



class Buyer_Account_Manager:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter=Delete_From_Table(con)
		self.updater=Update_Table(con)



	def change_location(self,location):
		self.updater.update_buyer_location(self.buyer_id,location)
		print("Buyer location has been changed")

	def view_buyer_history(self):
		history=self.displayer.display_history(self.buyer_id)
		print(history)

	def delete_account(self):
		self.deleter.delete_buyer_account(self.buyer_id)
		print("Account has been deleted")


class Buyer_Payment_Transactions:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter=Delete_From_Table(con)
		self.updater=Update_Table(con)



	def make_payment(self):
		pass


	def reduce_stock_of_purchase_items(self,product_name,seller_name,quantity_sold):
		product_id=self.getter.get_product_id(product_name)
		seller_id=self.getter.get_seller_id_by_name(seller_name)
		current_qty=self.getter.get_seller_product_qty(product_id,seller_id)
		Current_qty=self.getter.get_product_qty(product_id)
		self.updater.update_seller_qty(current_qty-quantity_sold,product_id,seller_id)
		self.updater.update_product(product_name,Current_qty-quantity_sold)
		print("Stock has been reduced")



class Buyer_Submit_Review:
	def __init__(self,con,name):
		self.getter=Get_From_Tables(con)
		self.displayer=Display_From_Table(con)
		self.adder=ADD_INTO_TABLES(con)
		self.buyer_name=name
		self.buyer_id=self.getter.get_buyer_id_by_name(self.buyer_name)
		self.deleter=Delete_From_Table(con)
		self.updater=Update_Table(con)



	def insert_into_history(self,order_id,date):
		order=self.displayer.display_order(order_id)
		print(order)
		if order == None:
			return 0
		order=order[0]
		print(order)
		self.adder.add_into_History(order[3],order[2],order[1],order[5],order[4],date)
		print("Order has been added to history")	



	def update_rating(self,seller_id,buyer_rating):
		rating=self.getter.get_seller_rating(seller_id)
		number_of_sales=self.getter.get_seller_number_of_sales(seller_id)
		print(number_of_sales)
		print(rating)
		new_rating=float((number_of_sales*rating)+buyer_rating)/(number_of_sales+1)
		self.updater.update_seller_number_of_sales(seller_id,number_of_sales+1)
		self.updater.update_seller_rating(seller_id,new_rating)
		print("rating has been updated")


	def delete_from_orders(self,id):
		self.deleter.delete_order(id)
		print("Order has been deleted")



#buyer1=Buyer_Search_Transactions(con)
#print(buyer1.Search_seller("Fotso"))
#print(buyer1.get_product_detail("Corn","Fos"))
#buyer2=Buyer_Cart_Manager(con,"Joe")
#print(buyer2.view_cart())
#buyer2.compute_sum()
#buyer2.empty_cart()
#buyer2.change_quantity(4,500)
#buyer4=Buyer_Account_Manager(con,"Auseni")
#buyer4.delete_account()
#buyer5=Buyer_Payment_Transactions(con,"Auseni")
#buyer5.reduce_stock_of_purchase_items("Vegetables","Fotso",88)
#buyer3=Buyer_Visit_Seller(con,"asnid")
#print(buyer3.visit_seller("Fos"))
buyer6=Buyer_Submit_Review(con,"Auseni")
#buyer6.update_rating(8,6)
buyer6.insert_into_history(7,"12-23-23")
#buyer6.delete_from_orders(5)
#first=ied[2]
#print(ied)
con.commit()
con.close()