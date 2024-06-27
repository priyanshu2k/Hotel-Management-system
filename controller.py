import os
import mysql.connector
from modules.room import Room
from modules.reservation import Reservation
from modules.auth import Auth
from modules.admin import Admin

# Configurations
from config import config
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=config.get("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=config.get("DB_NAME"),
        port="3306",
        autocommit=config.get("DB_AUTOCOMMIT"),
    )

    if connection.is_connected():
        print("Connection to the database was successful!")

    cursor = connection.cursor(buffered=True)

except mysql.connector.Error as err:
    print(f"Error: {err}")

cursor = connection.cursor(buffered=True)

username = ""
password = ""
role = ""


room_manager = Room(cursor)
reservation_manager = Reservation(cursor)
auth_manager = Auth(cursor)
admin = Admin(cursor, role)

count = 0
flag = False
role = ""

while(True):
    lst = auth_manager.checkUser()
    flag = lst[0]
    count+=1
    if count==5:
        cursor.close()
        connection.close()
        print("Limitation excedded, connection is closed")
        break
    if flag:
        role = lst[1]
        break  

# def deleteUser():
#     try:
#         username = input("Enter the username to delete: ")
#         cursor.execute(f"SELECT COUNT(*) FROM login WHERE username = '{username}';")
#         user_exists = cursor.fetchone()[0]

#         if user_exists:
#             # Prepare and execute the SQL delete query
#             cursor.execute(f"DELETE FROM login WHERE username = '{username}';")
#             connection.commit()
#             print("User deleted successfully!")
#         else:
#             print("User does not exist!")

#         return True

#     except Error as e:
#         print(f"Error: {e}")
#         return False


# def check_password_strength(password):
#     print(password)
#     # Check if password contains at least one lowercase letter, one uppercase letter, one digit, and one special character
#     if re.match(r"^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$", password):
#         return True
#     else:
#         return False

# def updatePassword():
#     try:
#         username = input("Enter your username: ")
        
#         # Verify if the username exists
#         cmd = f"SELECT sec_que, sec_ans FROM login WHERE username='{username}';"
#         cursor.execute(cmd)
#         result = cursor.fetchone()
        
#         if not result:
#             print("The username does not exist.")
#             return False
        
#         sec_que, sec_ans = result
#         print(f"Security Question: {sec_que}")
        
#         # Ask the user to answer the security question
#         user_answer = input("Enter your answer to the security question: ").strip()
        
#         if user_answer.lower() != sec_ans.lower():
#             print("Incorrect answer to the security question.")
#             return False
        
#         while True:
#             # Allow the user to set a new password securely
#             new_password = getpass.getpass("Enter your new password: ")

#             # if not check_password_strength(new_password):
#             #     print("Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")
#             #     continue
#             new_password=new_password.strip()
#             # Check password strength
            
            
#             # Hash the new password using SHA-256
#             hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            
#             # Update the hashed password in the database
#             cmd = f"UPDATE login SET password='{hashed_password}' WHERE username='{username}';"
#             cursor.execute(cmd)
            
#             # Commit the transaction
#             connection.commit()
            
#             print("Password has been reset successfully!")
#             return True

#     except mysql.connector.Error as err:
#         print(f"Database Error: {err}")
#         connection.rollback()
#         return False
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return False


if flag:
    print("Press 1 - Create a New Room")
    print("Press 2 - Show All Rooms")
    print("Press 3 - Show All Vacant Rooms")
    print("Press 4 - Show All Occupied Rooms")
    print("Press 5 - Make a reservation")
    print("Press 6 - Check Out")
    print("Press 7 - Show all reservations")
    print("Press 8 - Delete user(admin only)")
    print("Press 9 - Add user(admin only)")
    print("Press 10 - Update password")
    print("Press 11 - Add guest")
    print("Press 12 - Exit")


    while True:
        choice = int(input("Enter your choice : "))
        match choice:
            case 1:
                room_manager.createRoom()
            case 2:
                room_manager.showRooms()
            case 3:
                room_manager.showVacantRooms()
            case 4:
                room_manager.showOccupiedRooms()
            case 5:
                reservation_manager.makeReservation()
            case 6:
                reservation_manager.checkOut()
            case 7:
                reservation_manager.showReservations()
            case 8:
                admin.deleteUser()
            case 9:
                admin.addUser()    
            case 10:
                auth_manager.updatePassword()
            case 11:
                reservation_manager.addGuest()
            case 12:
                break   



    