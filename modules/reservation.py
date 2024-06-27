import mysql.connector

class Reservation:

    def __init__(self, cursor):
        self.cursor = cursor


    def addGuest(self):
        try:
            name = input("Enter guest name: ")
            address = input("Enter guest address: ")
            email_id = input("Enter guest email id: ")
            phone = int(input("Enter guest mobile number: "))

            # Prepare the SQL query
            cmd = f"INSERT INTO guests(name, address, email_id, phone) VALUES('{name}', '{address}', '{email_id}', {phone});"
            
            # Execute the SQL query
            self.cursor.execute(cmd)
            
            # Check if the guest was added
            if self.cursor.rowcount == 0:
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



    def makeReservation(self):
        g_id = input("Enter guest ID: ")
        meal = input("Enter meal option (0 or 1): ")
        r_id = input("Enter room ID: ")
        r_type = ""
        
        try:
            # Check if guest exists
            self.cursor.execute("SELECT id FROM guests WHERE id = %s", (g_id,))
            guest = self.cursor.fetchone()
        

            if not guest:
                print("Error: Guest ID does not exist.")
                return False

            # Check if room exists and is not currently booked
            self.cursor.execute("SELECT currently_booked, room_type FROM rooms WHERE id = %s", (r_id,))
            room = self.cursor.fetchone()
            if not room:
                print("Error: Room ID does not exist.")
                return False
            
            if room[0] == 1:
                print("Error: Room is currently booked.")
                return False
            
            r_type = room[1]
            # Insert reservation
            self.cursor.execute(
                "INSERT INTO reservations (g_id, meal, r_id, r_type) VALUES (%s, %s, %s, %s)",
                (g_id, meal, r_id, r_type)
            )
            
            # Check if the reservation was added
            if self.cursor.rowcount == 0:
                print("Error: Reservation failed.")
                return False


            print("Reservation done successfully!")
            return True

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False


    #  show reservations

    def showReservations(self):
        try:
            cmd = "SELECT id, g_id, r_id, r_type, check_in FROM reservations where check_out is NULL;"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
                return False
            
            res = self.cursor.fetchall()
            print("id  g_id  r_id  r_type  check_in")
            for row in res:
                print(row)
            return True
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False   


    def checkOut(self):
        try:
            guest_id = int(input("Enter the guest id: "))

            # Check if the guest exists and has a reservation
            cmd = f"SELECT r_id FROM reservations WHERE g_id={guest_id} AND check_out is NULL;"
            self.cursor.execute(cmd)
            result = self.cursor.fetchone()

            if not result:
                print("No active reservation found for this guest.")
                return False

            room_no = result[0]

            # Update the reservation to indicate the guest has checked out
            cmd = f"UPDATE reservations SET check_out=NOW() WHERE g_id={guest_id} AND r_id={room_no};"
            self.cursor.execute(cmd)

            # Update the room status to vacant
            cmd = f"UPDATE rooms SET currently_booked=0 WHERE id={room_no};"
            self.cursor.execute(cmd)

            # connection.commit()  # Commit the changes to the database

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
                