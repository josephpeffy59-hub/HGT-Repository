from BackEnd.Database_Manipulation_error_handling_version import ADD_INTO_TABLES
from BackEnd.Database_Manipulation_error_handling_version import Get_From_Tables
import sqlite3

class Agent_Login:
	def __init__(self,con):
		self.account_adder=ADD_INTO_TABLES(con)
		self.getter=Get_From_Tables(con)

	def login(self,name,id1):
		agent_id=self.getter.get_delivery_agent_id(name)
		print(agent_id)
		print("dfffffffffffffffffffs")
		if agent_id == id1:
			print("Successful Login")
			return 1

		else:
			print("No account match")
			return 0

#agent1=Agent_Login()
#agent1.login("asdfg",89)
