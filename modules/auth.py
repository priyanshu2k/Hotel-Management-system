import mysql.connector
import hashlib
import getpass
import re

class Auth:

    def __init__(self, cursor):
        self.cursor = cursor

    def checkUser(self):
        try:
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role, 1: admin, 2: user: ")
            if role=='1':
                role = 'admin'
            elif role=='2':
                role = 'user'

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # hashed_password = password
            print(hashed_password)
            cmd = f"SELECT COUNT(username) FROM login WHERE username='{username}' AND BINARY password='{hashed_password}' AND role='{role}'"
            self.cursor.execute(cmd)
            result = self.cursor.fetchone()
            if result and result[0] >= 1:
                print("Login successful")
                return [True, role]
            else:
                print("Invalid credentials")
                return [False, ""]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return [False, ""]
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return [False, ""]
        


    def check_password_strength(self, password):
        print(password)
        # Check if password contains at least one lowercase letter, one uppercase letter, one digit, and one special character
        if re.match(r"^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$", password):
            return True
        else:
            return False

    def updatePassword(self):
        try:
            username = input("Enter your username: ")
            
            # Verify if the username exists
            cmd = f"SELECT sec_que, sec_ans FROM login WHERE username='{username}';"
            self.cursor.execute(cmd)
            result = self.cursor.fetchone()
            
            if not result:
                print("The username does not exist.")
                return False
            
            sec_que, sec_ans = result
            print(f"Security Question: {sec_que}")
            
            # Ask the user to answer the security question
            user_answer = input("Enter your answer to the security question: ").strip()
            
            if user_answer.lower() != sec_ans.lower():
                print("Incorrect answer to the security question.")
                return False
            
            while True:
                # Allow the user to set a new password securely
                new_password = getpass.getpass("Enter your new password: ")

                new_password=new_password.strip()
                
                
                # Hash the new password using SHA-256
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                
                # Update the hashed password in the database
                cmd = f"UPDATE login SET password='{hashed_password}' WHERE username='{username}';"
                self.cursor.execute(cmd)
                
                # Commit the transaction
                # connection.commit()
                
                print("Password has been reset successfully!")
                return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            # connection.rollback()
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


