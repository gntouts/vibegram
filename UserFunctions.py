import sqlite3
import datetime
from dbclass import *
from DBHandling import *

def Create_Acc():
	##allows user to create an new acc and 
	##insert name, avatar, phone, email and password
	pass

def Sign_In():
	##allows user to sign in using his email and password
	##returns his user_id
	##changes users 'is_active' parameter
        found = 0
        while (not found):
            print ("----Sign In----")
            print ("Email: ", end='')
            email = input()
            print ("Password: ", end='')
            password = input()
            cur = c.execute("SELECT user_id FROM Users WHERE e_mail = :email AND password = :password", {"email":email, "password":password})
            for r in cur:
                found = r[0]
            if (not found):
                print ("Wrong username or password, try again!\n")
        return found
	
def Update_Account():
	##allows end user to change name, avatar, phone, email and password
	pass

def Add_Friend():
	##allows user to search and befriend another user
	##searches by name/phone/email/user_id
	pass
	
def Contact_List():
	##returns users contact list grouped by friend_type
	##also shows if contacts are active
	pass
	
def Create_Mess():
	##allows user to create new message and send it or save it as draft
	pass
	
def Send_Mess():
	##allows user to send message to One, Many or Group
	pass
	
def See_Conv():
	##allows user to see a conversation with a friend
	##also shows if past messages are delivered 
	##and their timestamp of delivery
	##makes all messages received by that user is_received
	pass
	
def Mess_Delivered():
	##absolutely no clue how to implement this
	pass
	
def Delete_Friend():
	##allows user to delete friend
	pass
	
def Change_friend_type(user_id, friend_id, new_type):
	##allows user to change friendship type
	with conn:
		c.execute("""UPDATE Users
				SET friend_type = :friend_tpe
				WHERE (friend1_id = :user_id 
				AND friend2_id = :friend_id)
				OR (friend2_id = :user_id 
				AND friend1_id = :friend_id)
				""",
				{'friend_type': new_type, 'friend1_id': name, 'friend2_id': lastname}
				)
	
def Delete_Account():
	##allows user to delete account
	##this deletes all his friendships
	##and changes all the messages sent or received by him
	##to sent/received by unknown
	pass
