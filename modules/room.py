import mysql.connector

class Room:
    def __init__(self, cursor):
        self.cursor = cursor

    def createRoom(self):
        try:
            room_no = int(input("Enter room number: "))
            price = int(input("Enter price: "))
            room_type = input("Enter room type, S: single, D: double: ").strip().upper()
            
            if room_type not in ('S', 'D'):
                raise ValueError("Invalid room type. Please enter 'S' for single or 'D' for double.")

            cmd = f"INSERT INTO rooms(room_no, price, room_type) VALUES({room_no}, {price}, '{room_type}');"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
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

    def showRooms(self):
        try:
            cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms;"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
                return False
            
            res = self.cursor.fetchall()
            print("id  room_no  room_type  price  created_at")
            for row in res:
                print(row)
            return True
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def showVacantRooms(self):
        try:
            cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms where currently_booked=0;"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
                return False
            
            res = self.cursor.fetchall()
            print("id  room_no  room_type  price  created_at")
            for row in res:
                print(row)
            return True
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def showOccupiedRooms(self):
        try:
            cmd = "SELECT id, room_no, room_type, price, created_at FROM rooms where currently_booked=1;"
            self.cursor.execute(cmd)
            
            if self.cursor.rowcount == 0:
                return False
            
            res = self.cursor.fetchall()
            print("id  room_no  room_type  price  created_at")
            for row in res:
                print(row)
            return True
        
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
