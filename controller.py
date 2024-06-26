import os
import mysql.connector
from mysql.connector import Error

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


# while True:
#     print(1)


def checkUser(username, password=None, role=None):
    try:
        cmd = f"SELECT COUNT(username) FROM login WHERE username='{username}' AND BINARY password='{password}' AND role='{role}'"
        cursor.execute(cmd)
        result = cursor.fetchone()
        if result and result[0] >= 1:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    

username = input("Enter username: ")
password = input("Enter password: ")
role = input("Enter role, 1: admin, 2: user: ")
if role=='1':
    role = 'admin'
elif role=='2':
    role = 'user'

if checkUser(username, password, role):
        print("Login successful")
else:
    print("Invalid credentials")



# create room
def createRoom():
    try:
        room_no = int(input("Enter room number: "))
        price = int(input("Enter price: "))
        room_type = input("Enter room type, S: single, D: double: ").strip().upper()
        
        if room_type not in ('S', 'D'):
            raise ValueError("Invalid room type. Please enter 'S' for single or 'D' for double.")

        cmd = f"INSERT INTO rooms(room_no, price, room_type) VALUES('{room_no}', {price}, '{room_type}');"
        cursor.execute(cmd)
        
        if cursor.rowcount == 0:
            return False
        
        print("New room created")
        return True

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return False
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False      



# show rooms

def showRooms():
    try:
        cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms;"
        cursor.execute(cmd)
        
        if cursor.rowcount == 0:
            return False
        
        res = cursor.fetchall()
        for row in res:
            print(row)
        return True
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    

 # show vacant rooms   

def showVacantRooms():
    try:
        cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms where currently_booked=0;"
        cursor.execute(cmd)
        
        if cursor.rowcount == 0:
            return False
        
        res = cursor.fetchall()
        for row in res:
            print(row)
        return True
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False



# show occupied rooms
def showOccupiedRooms():
    try:
        cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms where currently_booked=1;"
        cursor.execute(cmd)
        
        if cursor.rowcount == 0:
            return False
        
        res = cursor.fetchall()
        for row in res:
            print(row)
        return True
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# add guest
def addGuest():
    try:
        name = input("Enter guest name: ")
        address = input("Enter guest address: ")
        email_id = input("Enter guest email id: ")
        phone = int(input("Enter guest mobile number: "))

        # Prepare the SQL query
        cmd = f"INSERT INTO guests(name, address, email_id, phone) VALUES('{name}', '{address}', '{email_id}', {phone});"
        
        # Execute the SQL query
        cursor.execute(cmd)
        
        # Check if the guest was added
        if cursor.rowcount == 0:
            return False
        
        print("Guest added successfully!")
        return True

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return False
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# add reservation

def makeReservation():
    g_id = input("Enter guest ID: ")
    meal = input("Enter meal option (0 or 1): ")
    r_id = input("Enter room ID: ")
    r_type = input("Enter room type, S: single, D: double: ").strip().upper()
    
    try:
        # Check if guest exists
        cursor.execute("SELECT id FROM guests WHERE id = %s", (g_id,))
        guest = cursor.fetchone()
        if not guest:
            print("Error: Guest ID does not exist.")
            return False

        # Check if room exists and is not currently booked
        cursor.execute("SELECT currently_booked FROM rooms WHERE id = %s", (r_id,))
        room = cursor.fetchone()
        if not room:
            print("Error: Room ID does not exist.")
            return False
        if room[0] == 1:
            print("Error: Room is currently booked.")
            return False

        # Insert reservation
        cursor.execute(
            "INSERT INTO reservations (g_id, meal, r_id, r_type) VALUES (%s, %s, %s, %s)",
            (g_id, meal, r_id, r_type)
        )
        
        # Check if the reservation was added
        if cursor.rowcount == 0:
            print("Error: Reservation failed.")
            return False

        # Commit the transaction
        connection.commit()

        print("Reservation done successfully!")
        return True

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


#  show reservations

def showReservations():
    try:
        cmd = "SELECT id, g_id, r_id, r_type, check_in FROM reservations where check_out is NULL;"
        cursor.execute(cmd)
        
        if cursor.rowcount == 0:
            return False
        
        res = cursor.fetchall()
        for row in res:
            print(row)
        return True
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False        

# delete user

def deleteUser():
    try:
        username = input("Enter the username to delete: ")
        cursor.execute(f"SELECT COUNT(*) FROM login WHERE username = '{username}';")
        user_exists = cursor.fetchone()[0]

        if user_exists:
            # Prepare and execute the SQL delete query
            cursor.execute(f"DELETE FROM login WHERE username = '{username}';")
            connection.commit()
            print("User deleted successfully!")
        else:
            print("User does not exist!")

        return True

    except Error as e:
        print(f"Error: {e}")
        return False


#  check out

def checkOut():
    try:
        guest_id = int(input("Enter the guest id: "))

        # Check if the guest exists and has a reservation
        cmd = f"SELECT r_id FROM reservations WHERE g_id={guest_id} AND check_out is NULL;"
        cursor.execute(cmd)
        result = cursor.fetchone()

        if not result:
            print("No active reservation found for this guest.")
            return False

        room_no = result[0]

        # Update the reservation to indicate the guest has checked out
        cmd = f"UPDATE reservations SET check_out=NOW() WHERE g_id={guest_id} AND r_id={room_no};"
        cursor.execute(cmd)

        # Update the room status to vacant
        cmd = f"UPDATE rooms SET currently_booked=0 WHERE id={room_no};"
        cursor.execute(cmd)

        connection.commit()  # Commit the changes to the database

        print(f"Guest {guest_id} has checked out from room {room_no}.")
        return True

    except ValueError:
        print("Invalid input. Please enter a valid guest id.")
        return False
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    


print("Press 1 - Create a New Room")
print("Press 2 - Show All Rooms")
print("Press 3 - Show All Vacant Rooms")
print("Press 4 - Show All Occupied Rooms")
print("Press 5 - Make a reservation")
print("Press 6 - Check Out")
print("Press 7 - Show all reservations")
if role=='admin':
    print("Press 8 - Delete user")
print("Press 9 - Update password")
print("Press 10 - Add guest")
print("Press 11 - Exit")


while True:
    choice = int(input("Enter your choice : "))
    match choice:
        case 1:
            createRoom()
        case 2:
            showRooms()
        case 3:
            showVacantRooms()
        case 4:
            showOccupiedRooms()
        case 5:
            makeReservation()
        case 6:
            checkOut()
        case 7:
            showReservations()
        case 8:
            deleteUser()
        # case 9:
        #     updatePassword()
        case 10:
            addGuest()
        case 11:
            break   



  