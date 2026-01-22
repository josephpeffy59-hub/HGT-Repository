from BackEnd.Database_Manipulation_error_handling_version import ADD_INTO_TABLES
from BackEnd.Database_Manipulation_error_handling_version import Get_From_Tables
from BackEnd.Database_Manipulation_error_handling_version import Get_Database_connection
import re
import os
import sqlite3

class Buyer_Login:
    def __init__(self):
        # We establish a local connection for this instance
        self.con = Get_Database_connection()
        
        # Pass the connection to your manipulation classes
        self.account_adder = ADD_INTO_TABLES(self.con)
        self.getter = Get_From_Tables(self.con)

    def validate_password(self, password):
        if 7 < len(password) < 16:
            if re.search("[^a-zA-Z]", password):
                return 1
            else:
                return 0
        else:
            return 0

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return 1
        else:
            return 0

    def create_buyer_account(self, name, e_mail, location, phone, password, date_of_creation):
        if self.validate_password(password):
            if self.validate_email(e_mail):
                if self.getter.get_buyer_id_by_email(e_mail) is None:
                    self.account_adder.add_into_buyer_account(name, e_mail, location, phone, password, date_of_creation)
                    self.con.commit() # Save changes to the DB
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

    def get_buyer_id(self, name):
        ID = self.getter.get_buyer_id_by_name(name)
        return ID

    def login(self, name, e_mail, password):
        email_id = self.getter.get_buyer_id_by_email(e_mail)
        Password_id = self.getter.get_buyer_id_by_password(password)
        name_id = self.getter.get_buyer_id_by_name(name)
        
        if email_id is None:
            print("Account not found")
            return "Account not found"
        elif email_id == Password_id and email_id == name_id:
            print("Account found!!")
            return 1
        elif email_id is not None and email_id != Password_id:
            print("Wrong password")
            return "Wrong password"
        elif email_id is not None and name_id != email_id:
            print("Wrong username!!")
            return "Wrong username!!"
        else:
            return 1

    def Get_buyer_info(self, name):
        ID = self.getter.get_buyer_id_by_name(name)
        info = self.getter.get_buyer_info(ID)
        return info

    def close_connection(self):
        """Call this to safely close the server connection"""
        self.con.close()


#login1=Buyer_Login(con)
#login1.create_buyer_account("asind","ysh2jsdj@sdf.asd","buan",8998988,"as@es12g","12-23-23")
