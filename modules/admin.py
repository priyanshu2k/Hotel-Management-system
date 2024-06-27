import mysql.connector
from mysql.connector import Error
import hashlib
import getpass
import re

class Admin:
    def __init__(self, cursor, role):
        self.cursor = cursor
        self.role = role

    def deleteUser(self):
        try:
            if self.role=='user':
                print("Not an admin")
                return False
            username = input("Enter the username to delete: ")
            self.cursor.execute(f"SELECT COUNT(*) FROM login WHERE username = '{username}';")
            user_exists = self.cursor.fetchone()[0]

            if user_exists:
                # Prepare and execute the SQL delete query
                self.cursor.execute(f"DELETE FROM login WHERE username = '{username}';")
                print("User deleted successfully!")
            else:
                print("User does not exist!")

            return True

        except Error as e:
            print(f"Error: {e}")
            return False
        

    def addUser(self):
        try:
            # print(self.role)
            if self.role=="user":
                print("Not an admin")
                return False
            username = ""
            password = ""
            role = ""

            username = input("Enter a new username: ")
            password =input("Enter password: ")
            role = input("Enter the user role: ")
            print(self.role)

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cmd = f"INSERT INTO login(username, password, role) VALUES('{username}', '{hashed_password}', '{role}');"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
                return False
            
            print("New user created")
            return True

        except Error as e:
            print(f"Error: {e}")
            return False    