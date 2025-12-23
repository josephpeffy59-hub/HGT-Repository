from Database_Manipulation import ADD_INTO_TABLES
from Database_Manipulation import Get_From_Tables
import re
class Seller_Login:
	def __init__(self):
		self.account_adder=ADD_INTO_TABLES()
		self.getter=Get_From_Tables()


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




	def create_seller_account(self,name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation):
		if self.validate_password(password):
			if self.validate_email(e_mail):
				if self.getter.get_seller_id_by_email(e_mail)== None:
					self.account_adder.add_into_seller_account(name,buisness_name,buisness_type,phone,e_mail,password,location,open_time,rating,number_of_sales,date_of_creation)
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

	def login(self,name,e_mail):
		if self.getter.get_seller_id_by_email(e_mail)== None:
			return 1

		else:
			return "account not found"
		

login1=Seller_Login()
login1.create_seller_account("Fotso","bosso","Supermarket",677978598,"Yownow@gmail.com","Sas@es12g","Bastos","3:00",4,67,"12-12-12")