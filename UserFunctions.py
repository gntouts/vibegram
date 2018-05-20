import sqlite3
import datetime
from dbclass import *
from DBHandling import *

def Check_if_exists(user_mail):
	id = search_by_email(user_mail)
	##if....


def Create_Acc(c):##
	##allows user to create an new acc and 
    ##insert name, avatar, phone, email and password
    print ("----Sign Up----")
    print ("Name: ", end='')
    name = input()
    print ("Last Name: ", end='')
    lastname = input()
    print ("Email: ", end='')
    email = input()
    print ("Phone: ", end='')
    phone = input()
    print ("Password: ", end='')
    password = input()
    print ("Avatar: ", end='')
    avatar = input()

    print ("Creating account...")
    user = Users('', name, lastname, avatar, phone, \
                 email, password, dt.datetime.now() , 'y')

    ins_user(user)
    cur = c.execute("SELECT user_id FROM Users WHERE e_mail = :email AND password = :password", {"email":email, "password":password})
    for r in cur:
        uid = r[0]
    return uid


def Sign_In(c):
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
	
def Update_Account(userid, c):
	##allows end user to change name, avatar, phone, email and password
    a = -1
    while (a not in range(7)):
        print ("Choose what to change: ")
        print ("1) Email")
        print ("2) Password")
        print ("3) Name")
        print ("4) Last Name")
        print ("5) Avatar")
        print ("6) Phone")
        print ("0) Go Back")
        a = int(input())
        if (a==1):
            print ("Email: ", end='')
            email = input()
            c.execute("""UPDATE Users SET e_mail = :email
                        WHERE user_id = :userid""", \
                      {"email" : email, "userid" : userid})
        elif (a==2):
            print ("Password: ", end='')
            password = input()
            c.execute("""UPDATE Users SET password = :password
                        WHERE user_id = :userid""", \
                      {"password" : password, "userid" : userid})
        elif (a==3):
            print ("Name: ", end='')
            name = input()
            c.execute("""UPDATE Users SET first_name = :name
                        WHERE user_id = :userid""", \
                      {"name" : name, "userid" : userid})
        elif (a==4):
            print ("Last Name: ", end='')
            lastname = input()
            c.execute("""UPDATE Users SET last_name = :lastname
                        WHERE user_id = :userid""", \
                      {"lastname" : lastname, "userid" : userid})
        elif (a==5):
            print ("Avatar: ", end='')
            avatar = input()
            c.execute("""UPDATE Users SET avatar = :avatar
                        WHERE user_id = :userid""", \
                      {"avatar" : avatar, "userid" : userid})
        elif (a==6):
            print ("Phone: ", end='')
            phone = input()
            c.execute("""UPDATE Users SET phone_number = :phone
                        WHERE user_id = :userid""", \
                      {"phone" : phone, "userid" : userid})
        else:
              pass

        if (a):
              print ("Profile updated successfully!")

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
	
def Delete_Friend(user_id, friend_id):
	##allows user to delete friend
	with conn:
		c.execute("""DELETE from Friend
					WHERE (friend1_id = :user_id AND friend2_id = :friend_id)
					OR (friend2_id = :user_id AND friend1_id = :friend_id)""",
					{'user_id': user_id, 'friend_id': friend2_id}
					)
	
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
	
def Delete_Account(user_id):
	##allows user to delete account
	##this deletes all his friendships
	##and changes all the messages sent or received by him
	##to sent/received by unknown
	with conn:
		deleted_id = 'UNKNOWN'
		
		c.execute("DELETE from Users WHERE user_id = :user_id",
                  {'user_id': user_id})
		c.execute("""DELETE from Friend
					WHERE friend1_id = :user_id OR friend2_id = :user_id""",
					{'user_id': user_id}
					)
		c.execute("""UPDATE Messages
					SET sender_id = :deleted_id
					WHERE sender_id = :user_id""",
					{'deleted_id': deleted_id, 'user_id': user_id}
					)
		c.execute("""UPDATE Receiving
					SET recipient_id = :deleted_id
					WHERE recipient_id = :user_id""",
					{'deleted_id': deleted_id, 'user_id': user_id}
					)		
					
					
