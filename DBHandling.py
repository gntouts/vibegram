import sqlite3
from dbclass import *

conn = sqlite3.connect('vibegram.db')

c = conn.cursor()

# c.execute("""CREATE TABLE Users (
                # user_id integer PRIMARY KEY AUTOINCREMENT,
		# first_name varchar,
		# last_name varchar,
		# avatar blob,
		# phone_number varchar,
		# e_mail varchar,
		# password varchar,
		# created_account datetime,
		# is_active varchar
		# )
		# """)
   
# c.execute("""CREATE TABLE Friend (
			# friendship_ID integer PRIMARY KEY AUTOINCREMENT,
			# friend1_ID integer,
			# friend2_ID integer,
			# date_added datetime,
			# friend_type varchar
			# )
			# """)
			
# c.execute("""CREATE TABLE Messages (
			# message_ID integer PRIMARY KEY AUTOINCREMENT,
			# sender_ID integer,
			# is_sent varchar,
			# date_time_sent datetime,
			# message_body text,
			# attachment blob
			# )
			# """)
			
# c.execute("""CREATE TABLE Receiving (			
			# recipient_ID integer,
			# date_time_received datetime,
			# is_received varchar,
			# message_ID integer
			# )
			# """)
			
def ins_user(user):
	with conn:
		c.execute("INSERT INTO Users (first_name, last_name, avatar, phone_number, e_mail, password, created_account, is_active) VALUES (:first_name, :last_name, :avatar, :phone_number, :e_mail, :password, :created_account, :is_active)", {'first_name': user.first_name, 'last_name': user.last_name, 'avatar': user.avatar, 'phone_number': user.phone_number, 'e_mail': user.e_mail, 'password': user.password, 'created_account': user.created_account, 'is_active': user.is_active})
		
def clear_users():
	with conn:
		c.execute("DELETE FROM Users")
		
def del_user(user):
	with conn:
		c.execute("DELETE from Users WHERE first_name = :first_name AND last_name = :last_name",
                  {'first_name': user.first_name, 'last': user.last_name})
				  

def print_users():
	with conn:
		c.execute("SELECT * FROM Users")
		print(c.fetchall())
