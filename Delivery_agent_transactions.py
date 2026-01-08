from BackEnd.Database_Manipulation_error_handling_version import *
class delivery:
	def __init__(self,con,id1):
		self.displayer=Display_From_Table(con)
		self.agent_id=id1
		self.getter=Get_From_Tables(con)


	def display_orders(self):
		orders=self.displayer.display_delivery_agent_orders(self.agent_id)
		print(orders)
		print("******************************************88")
		Orders=[]
		for order in orders:
			order=list(order)
			order[1]=self.getter.get_product_name_by_id(order[1])
			order[4]=self.getter.get_buyer_name_by_id(order[4])
			Orders.append(order)
		return Orders
	

	def display_history(self):
		history=display_delivery_agent_history(self.agent_id)
		if history:
			print(history)
			return history
		else:
			return None
	

