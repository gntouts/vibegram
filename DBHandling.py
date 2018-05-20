import sqlite3
import datetime
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
                             friendship_id integer PRIMARY KEY AUTOINCREMENT,
                             friend1_id integer,
                             friend2_id integer,
                             date_added datetime,
                             friend_type varchar
                             );
                             """)
                            
    c.execute("""CREATE TABLE IF NOT EXISTS Messages (
                             message_id integer PRIMARY KEY AUTOINCREMENT,
                             sender_id integer,
                             is_sent varchar,
                             date_time_sent datetime,
                             message_body text,
                             attachment blob
                             );
                             """)
                            
    c.execute("""CREATE TABLE IF NOT EXISTS Receiving (			
                             recipient_id integer,
                             date_time_received datetime,
                             is_received varchar,
                             message_id integer
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
		
def del_user_by_name(user):
	with conn:
		c.execute("DELETE from Users WHERE first_name = :first_name AND last_name = :last_name",
                  {'first_name': user.first_name, 'last': user.last_name})
				  
				  
def del_user_by_id(user):
	with conn:
		c.execute("DELETE from Users WHERE user_id = :user_id ",
                  {'user_id': user.user_id})

def print_users():
	with conn:
		c.execute("SELECT * FROM Users")
		print(c.fetchall())
		
def print_usnames():
	with conn:
		c.execute("SELECT user_id, first_name, last_name FROM Users")
		print(c.fetchall())
				  
def make_friend(user1_id, user2_id, friend_type):
	with conn:
		date_added = str(datetime.datetime.now())
		c.execute("""INSERT INTO Friend (friend1_id, 
		friend2_id, date_added, friend_type) 
		
		VALUES (:friend1_id, :friend2_id,
		:date_added, 
		:friend_type)""",
		{'friend1_id':user1_id, 
		'friend2_id': user2_id, 
		'date_added': date_added, 
		'friend_type': friend_type})
				
def print_friends():
	with conn:
		c.execute("SELECT * FROM Friend")
		print(c.fetchall())

		
def delete_friend(user1_id, user2_id):
	with conn:
		c.execute("DELETE from Friend WHERE friend1_id = :friend1_id AND friend2_id = :friend2_id",
                  {'friend1_id': user2_id, 'friend2_id': user1_id})
		
def clear_friends():
	with conn:
		c.execute("DELETE FROM Friend")

def search_by_name(name, lastname):
	with conn:
		c.execute("""SELECT user_id FROM Users
					WHERE first_name = :first_name 
					AND last_name = :last_name""",
					{'first_name': name, 'last_name': lastname}
					)
		print(c.fetchall())
		
def search_first(name):
	with conn:
		c.execute("""SELECT user_id FROM Users
					WHERE first_name = :first_name""",
					{'first_name': name}
					)
		print(c.fetchall())
		
def search_last(lastname):
	with conn:
		c.execute("""SELECT user_id FROM Users
					WHERE last_name = :last_name""",
					{'last_name': lastname}
					)
		print(c.fetchall())
				
def search_by_phone(phone):
	with conn:
		c.execute("""SELECT user_id FROM Users
					WHERE phone_number = :phone_number""",
					{'phone_number': number}
					)
		print(c.fetchall())
		
		
def search_by_email(email):
	with conn:
		c.execute("""SELECT user_id FROM Users
					WHERE e_mail = :pe_mail""",
					{'e_mail': email}
					)
		print(c.fetchall())
		
def create_message(message):
	with conn:
		date_sent = str(datetime.datetime.now())
		c.execute("""INSERT INTO Messages (sender_id,
		is_sent, date_time_sent,
		message_body, attachment)
		
		VALUES (:sender_id,
		:is_sent, 
		:date_time_sent,
		:message_body, 
		:attachment)""",
		{'sender_id': message.sender_id,
		'is_sent': message.is_sent, 'date_time_sent': date_sent,
		'message_body': message.message_body, 'attachment': message.attachment}
		)

def send_message(recipient_id, message_id):
	with conn:
		c.execute("""INSERT INTO Receiving (recipient_id,
		date_time_received, is_received,
		message_id)
		
		VALUES (:recipient_id,
		:date_time_received, 
		:is_received,
		:message_id)""",
		{'recipient_id': recipient_id,
		'date_time_received': '', 'is_received': 'N',
		'message_id': message_id}
		)

def send_to_many(recipient_id_list, message_id):	
	##count = len(id_list)
	for recipient in recipient_id_list:
		send_message(recipient, message_id)
		
def send_to_group(group, message_id):
	with conn:
		c.execute("""SELECT sender_id FROM Messag
					WHERE message_id = :message_id""",
					{'message_id': message_id}
					)
		sender_id = c.fetchone()
		c.execute("""SELECT friend1_id
				FROM Messages
				WHERE (friend2_id = :sender_id AND friend_type = :friend_type)""",
				{'sender_id': sender_id, 'friend_type': group}
				)
		recipients1 = c.fetchall()
		c.execute("""SELECT friend2_id
				FROM Messages
				WHERE (friend1_id = :sender_id AND friend_type = :friend_type)""",
				{'sender_id': sender_id, 'friend_type': group}
				)
		recipients2 = c.fetchall()
		send_to_many(recipients1, message_id)
		send_to_many(recipients2, message_id)
		
		
def message_received(message_id):
	with conn:
		date_time_received = str(datetime.datetime.now())
		is_received = 'Y'
		c.execute("""UPDATE Receiving
		SET date_time_received = :date_time_received, is_received = :is_received
		WHERE message_id  = :message_id)""",
		{'date_time_received': date_time_received,
		'is_received': is_received,
		'message_id': message_id}
		)
		

def print_all_msg():
	with conn:
		c.execute("SELECT * FROM Messages")
		print(c.fetchall())		

def print_conv(user1_id, user2_id):
	with conn:
		c.execute("""SELECT  sender_id, message_body, attachment
			FROM Messages JOIN Receiving
			ON Receiving.message_id = Messages.message_id
			WHERE (sender_id = :sender_id AND recipient_id = :recipient_id)
			OR (sender_id = :recipient_id AND recipient_id = :sender_id)
			ORDER BY Receiving.date_time_received DESC
			""",
			{'recipient_id': user1_id, 'sender_id': user2_id}
			)
		print(c.fetchmany(20))


##clear_users()
		
##user1 = Users('', 'Giorgos', 'Tasopoulos', 's', 2106014255, 'tasop@gmail.com', 'passkey', 's', 'y')
##user2 = Users('', 'Zoi', 'Tzavlanis', 's', 2101314255, 'zavl@gmail.com', 'passkey', 's', 'y')
##user3 = Users('', 'Dora', 'Sips', 's', 2106014255, 'tsips@gmail.com', 'passkey', 's', 'y')
##user4 = Users('', 'Spiros', 'Katsen', 's', 2101314255, 'katsen@gmail.com', 'passkey', 's', 'y')
##user5 = Users('', 'Konsta', 'Alexiu', 's', 2106014255, 'alex@gmail@gmail.com', 'passkey', 's', 'y')
##user6 = Users('', 'Dimitre', 'Dim', 's', 2101314255, 'dim@gmail.com', 'passkey', 's', 'y')

##print(user1)
##CreateTables(c)

##ins_user(user1)
##ins_user(user2)
##ins_user(user3)
##ins_user(user4)
##ins_user(user5)
##ins_user(user6)

##print_users()
##users = print_usnames()

##make_friend(2, 5, 'work')
##print_friends()

##body = 'Ola kala file?'
##message1=Messages('',2, 'Y', '', body, '/0')
##create_message(message1)
##print_all_msg()
#print_conv(2, 2)
