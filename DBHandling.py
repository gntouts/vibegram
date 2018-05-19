import sqlite3
from dbclass import *

conn = sqlite3.connect('vibegram.db')

c = conn.cursor()

def CreateTables(c):
    c.execute("""CREATE TABLE IF NOT EXISTS Users (
                 user_id integer PRIMARY KEY AUTOINCREMENT,
		 first_name varchar,
		 last_name varchar,
		 avatar blob,
		 phone_number varchar,
		 e_mail varchar,
		 password varchar,
		 created_account datetime,
		 is_active varchar
		 );
		 """)
   
    c.execute("""CREATE TABLE IF NOT EXISTS Friend (
                             friendship_ID integer PRIMARY KEY AUTOINCREMENT,
                             friend1_ID integer,
                             friend2_ID integer,
                             date_added datetime,
                             friend_type varchar
                             );
                             """)
                            
    c.execute("""CREATE TABLE IF NOT EXISTS Messages (
                             message_ID integer PRIMARY KEY AUTOINCREMENT,
                             sender_ID integer,
                             is_sent varchar,
                             date_time_sent datetime,
                             message_body text,
                             attachment blob
                             );
                             """)
                            
    c.execute("""CREATE TABLE IF NOT EXISTS Receiving (			
                             recipient_ID integer,
                             date_time_received datetime,
                             is_received varchar,
                             message_ID integer
                             );
                             """)
			
			
def ins_user(user):
	with conn:
		c.execute("""INSERT INTO Users (first_name,
                            last_name, avatar,
                            phone_number,
                            e_mail,
                            password,
                            created_account,
                            is_active)
                            
                            VALUES (:first_name,
                            :last_name,
                            :avatar,
                            :phone_number,
                            :e_mail,
                            :password,
                            :created_account,
                            :is_active)""",
                            {'first_name': user.first_name, 'last_name': user.last_name,
                            'avatar': user.avatar, 'phone_number': user.phone_number,
                            'e_mail': user.e_mail, 'password': user.password,
                            'created_account': user.created_account, 'is_active': user.is_active})
		
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
		
def print_usnames():
	with conn:
		c.execute("SELECT user_id, first_name, last_name FROM Users")
		print(c.fetchall())
				  
def make_friend(user1_id, user2_id, date_added, friend_type):
	with conn:
		c.execute("""INSERT INTO Friend (friend1_id, 
		friend2_id, date_added, friend_type) 
		
		VALUES (:friend1_id, :friend2_id,
		:date_added, 
		:friend_type)""",
		{'friend1_id':user1_id, 
		'friend2_id': user2_id, 
		'date_added': date_added, 
		'friend_type': friend_type})
		conn.commit
		
		
def print_friends():
	with conn:
		c.execute("SELECT * FROM Friend")
		print(c.fetchall())


clear_users()
		
user1 = Users('', 'Giorgos', 'Tasopoulos', 's', 2106014255, 'tasop@gmail.com', 'passkey', 's', 'y')
user2 = Users('', 'Zoi', 'Tzavlanis', 's', 2101314255, 'zavl@gmail.com', 'passkey', 's', 'y')
user3 = Users('', 'Dora', 'Sips', 's', 2106014255, 'tsips@gmail.com', 'passkey', 's', 'y')
user4 = Users('', 'Spiros', 'Katsen', 's', 2101314255, 'katsen@gmail.com', 'passkey', 's', 'y')
user5 = Users('', 'Konsta', 'Alexiu', 's', 2106014255, 'alex@gmail@gmail.com', 'passkey', 's', 'y')
user6 = Users('', 'Dimitre', 'Dim', 's', 2101314255, 'dim@gmail.com', 'passkey', 's', 'y')

print(user1)

ins_user(user1)
ins_user(user2)
ins_user(user3)
ins_user(user4)
ins_user(user5)
ins_user(user6)

##print_users()
users = print_usnames()

make_friend(217, 216, '29.12.1995', 'work')
##print_friends()
