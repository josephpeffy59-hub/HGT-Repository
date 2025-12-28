#This is Buyer_Login
from Database_Manipulation import ADD_INTO_TABLES
from Database_Manipulation import Get_From_Tables
import re
import os
import sqlite3
con= sqlite3.connect("GrabNGo_Database.db")

class Buyer_Login:
	def __init__(self,con):
		self.account_adder=ADD_INTO_TABLES(con)
		self.getter=Get_From_Tables(con)
		print(os.path.abspath("GrabNGo_Database.db"))



	def validate_password(self,password):
		if 7<len(password)<16:
			if re.search("[^a-zA-Z]",password):
				return 1

			else:
				return 0

		else:
			return 0


	def validate_email(self,email):
		pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
		if re.match(pattern, email):
			return True
		else:
			return False



	def create_buyer_account(self,name,e_mail,location,phone,password,date_of_creation):
		if self.validate_password(password):
			if self.validate_email(e_mail):
				if self.getter.get_buyer_id_by_email(e_mail)== None:
					self.account_adder.add_into_buyer_account(name,e_mail,location,phone,password,date_of_creation)
					print("Account created")
					return 1

				else:
					print("account already exist!!")
					return "account already exist!!"


			else:
				print("Invalid email")
				return "Invalid email"


		else:
			print("Invalid password")
			return "Invalid password"


	def login(self,name,e_mail):
		if self.getter.get_buyer_id_by_email(e_mail) != None:
			return 1

		else:
			return "account not found"



login1=Buyer_Login(con)
login1.create_buyer_account("asind","ysh2jsdj@sdf.asd","buan",8998988,"as@es12g","12-23-23")
con.commit()
con.close()