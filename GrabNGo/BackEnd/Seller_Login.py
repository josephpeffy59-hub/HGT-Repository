#This is Seller_Login
from BackEnd.Database_Manipulation_error_handling_version import ADD_INTO_TABLES
from BackEnd.Database_Manipulation_error_handling_version import Get_From_Tables
from BackEnd.Database_Manipulation_error_handling_version import Get_Database_connection
import re
import os
import sqlite3

class Seller_Login:
	def __init__(self):
		# Initialize connection internally using your function
		self.con = Get_Database_connection()
		self.account_adder = ADD_INTO_TABLES(self.con)
		self.getter = Get_From_Tables(self.con)


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


	def create_seller_account(self,name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation,img):
		if self.validate_password(password):
			if self.validate_email(e_mail):
				if self.getter.get_seller_id_by_email(e_mail)== None:
					self.account_adder.add_into_seller_account(name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation,img)
					# Ensure the account is saved to the DB
					self.con.commit()
					print("Account created")
					return 1

				else:
					print("Account already exist")
					return "account already exist!!"

			else:
				print("Invalid Email")
				return "Invalid email"

		else:
			print("Invalid password")
			return "Invalid password"

	def Get_seller_info(self,name):
		ID=self.getter.get_seller_id_by_name(name)
		info=self.getter.get_seller_info(ID)
		return info

	def get_seller_id(self,name):
		ID=self.getter.get_seller_id_by_name(name)
		return ID

	def login(self,name,e_mail,password):
		email_id =self.getter.get_seller_id_by_email(e_mail)
		Password_id=self.getter.get_seller_id_by_password(password)
		name_id=self.getter.get_seller_id_by_name(name)
		print("*******************")
		print(email_id)
		print(Password_id)
		print(name_id)
		print("*******************")

		if  email_id == None:
			print("Account not found")
			return "Account not Found"
		elif email_id != None and email_id==Password_id and email_id==name_id:
			print("Account found!!")
			return 1
		elif email_id != None and email_id!=Password_id:
			print("Wrong password")
			return "Wrong Password"
		elif email_id!=None and email_id!=name_id:
			print("Wrong username!!")
			return "Invalid Username"
		else:
			return 1

	def close_connection(self):
		"""Call this to safely close the server connection"""
		self.con.close()
