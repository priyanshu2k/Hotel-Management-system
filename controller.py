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
role = ""

room_manager = Room(cursor)
reservation_manager = Reservation(cursor)
auth_manager = Auth(cursor)


count = 0
flag = False


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





admin = Admin(cursor, role)


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



    