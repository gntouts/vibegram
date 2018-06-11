import sqlite3
import datetime as dt
import random
import hashlib, getpass
from CreateDB import *

conn = sqlite3.connect('vibegram.db')

def cls(): print ("\n" * 100)

def Sign_In():
    ##allows user to sign in using his email and password
    ##returns his user_id
    ##changes users 'is_active' parameter
    with conn:
        c = conn.cursor()
        found = 0
        while (not found):
            print ("----Sign In----")
            print("To go back press enter")
            print ("Email: ", end='')
            email = input()
            if (not email):
                return 0
            else:
                #------------Password hashing---------------
                #print ("Password: ", end='')
                raw_password = getpass.getpass()

                cur = c.execute("""SELECT password FROM User
                                WHERE e_mail = :email """,
                                {"email":email})
                #aqcuires salt from saved password
                for r in cur:
                    salt = r[0][:5]
                #hashes salt and given password
                hsh = hashlib.sha256(('%s%s' % (salt, raw_password)).encode('utf-8')).hexdigest()
                final_password = '%s$%s' % (salt, hsh)
                #-------------------------------------------
                cur = c.execute("""SELECT user_id FROM User
                                WHERE e_mail = :email AND password = :password""",
                                {"email":email, "password":final_password})
                
                for r in cur:
                    found = r[0]
                        
                if (not found):
                    print ("Wrong username or password, try again!\n")
                else:
                    c.execute("""UPDATE User SET is_active = 'y'
                                    WHERE user_id = :user_id;""",
                                      {"user_id" : found})
                    
                return found
    
def Create_Acc():
    ##allows user to create an new acc and 
    ##insert name, avatar, phone, email and password
    with conn:
        c = conn.cursor()
        print ("----Sign Up----")
        print("To go back press enter")
        print ("Name: ", end='')
        name = input()
        if (not name):
            uid = 0
            return 0
        else:
            print ("Last Name: ", end='')
            lastname = input()
            print ("Email: ", end='')
            email = input()
            print ("Phone: ", end='')
            phone = input()
            #------------Password hashing---------------
            
            print ("Password: ", end='')
            raw_password = input()
            salt = hashlib.sha256(str(random.getrandbits(512)).encode('utf-8')).hexdigest()[:5]
            hsh = hashlib.sha256(('%s%s' % (salt, raw_password)).encode('utf-8')).hexdigest()
            final_password = '%s$%s' % (salt, hsh)
            
            #-----------------------------------------
            print ("Avatar: ", end='')
            avatar = input()

            print ("Creating account...")

            Ins_User(name, lastname, avatar, phone, \
                         email, final_password, dt.datetime.now() , 'y')
            cur = c.execute("SELECT user_id FROM User WHERE e_mail = :email AND password = :password", {"email":email, "password":final_password})
            for r in cur:
                uid = r[0]
            return uid
        
    
    
def Ins_User(name, lastname, avatar, phone, \
             email, password, ora , is_active):
    with conn:
        c = conn.cursor()
        c.execute("""INSERT INTO User (first_name,
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
                    {'first_name': name, 'last_name': lastname,
                    'avatar': avatar, 'phone_number': phone,
                    'e_mail': email, 'password': password,
                    'created_account': ora, 'is_active': is_active})
                                                    
													
													
def Search_Users():
    with conn:
        c = conn.cursor()
        results = ['0']
        a=-1
        while (a not in range(4)):
            print ("\n1) Search users by fist name")
            print ("2) Search users by last name")
            print ("3) Search users by e-mail")
            print ("0) Back")
            print ("What would you like to do: ", end='')
            a = int(input())

        print ("Search: ", end="")
        if (a == 1):
            words = input()
            Search_First(words, results)
        elif (a == 2):
            words = input()
            Search_Last(words, results)
        elif (a == 3):
            words = input()
            Search_Email(words, results)
        else:
            pass

        if (a != 0):
            for i in range(1, len (results)):
                print (i, end=' ')
                Print_Usnames(results[i])
            return results
        else:
            return []
  

def Search_First(name, results):
    name = "%" + name + "%"
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT user_id FROM User
                            WHERE first_name LIKE :first_name""",
                            {'first_name': name}
                            )
        for r in cur:
            results.append(r)

def Search_Last(lastname, results):
    lastname = "%" + lastname + "%"
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT user_id FROM User
                            WHERE last_name LIKE :last_name""",
                            {'last_name': lastname}
                            )
        for r in cur:
            results.append(r)
            
def Search_Email(email, results):
    email = "%" + email + "%"
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT user_id FROM User
                            WHERE e_mail LIKE :e_mail""",
                            {'e_mail': email}
                            )
        for r in cur:
            results.append(r)
            
def Print_Usnames(r):
    with conn:
        c = conn.cursor()
        cur = c.execute("SELECT user_id, first_name, last_name FROM User WHERE user_id = ?", (r[0],))
        for r in cur:
            print (r[1], r[2])
                
        
def Add_Friend(a, userid1,userid2, friendtype):
    ##allows user to search and befriend another user
    ##searches by name/phone/email/user_id
    with conn:
        c = conn.cursor()
        if (a):
            c.execute("""INSERT INTO Friend (friend1_id, friend2_id,
                          date_added, friend_type)
                          VALUES (:friend1_id, :friend2_id,
                          :date_added, :friend_type)""",
                          {"friend1_id" : userid1, "friend2_id" : userid2,
                          "date_added" : dt.datetime.now(), "friend_type" : friendtype})


def Contact_List(userid):
    ##returns users contact list grouped by friend_type
    ##also shows if contacts are active
    #Users.first_name, Users.last_name, Users.is_active
    #JOIN Users ON Friend.friend2_id = Users.user_id)
    results=["0"]
    i = 1
    with conn:  
        c = conn.cursor()
        cur = c.execute("""SELECT DISTINCT U.user_id, U.first_name, U.last_name, U.is_active,
                        User.user_id, User.first_name, User.last_name, User.is_active, Friend.friend_type
                        FROM ( (User as U) JOIN
                        (Friend JOIN User ON Friend.friend1_id = User.user_id)
                        ON U.user_id = Friend.friend2_id)
                        WHERE Friend.friend2_id = :userid OR Friend.friend1_id = :userid;""",
                        {"userid" : userid, "userid" : userid})
        print ("\n----Friends-----")
        for r in cur:
            #elegxos wste na mhn ektypwnei to onoma sou alla to onoma tou filou sou
            print(i, ") ", end="")
            i = i + 1
            if (r[0] == userid):
                #elegxos ama o filos einai active
                if (r[7] == 'y'):
                    print (r[5], r[6], r[8], "Active")
                else:
                    print (r[5], r[6], r[8], "Inactive")
                results.append(r[4])
            else:
                
                if (r[3] == 'y'):
                    print (r[1], r[2], r[8], "Active")
                else:
                    print (r[1], r[2], r[8], "Inactive")
                results.append(r[0])
        return results

		
def Create_Message(body, userid):
    with conn:
        c = conn.cursor()
        date_sent = str(dt.datetime.now())
        c.execute("""INSERT INTO Message (sender_id,
        is_sent, date_time_sent,
        message_body)

        VALUES (:sender_id,
        :is_sent, 
        :date_time_sent,
        :message_body)""",
        {'sender_id': userid,
        'is_sent': 'n', 'date_time_sent': date_sent,
        'message_body': body}
        )
        return date_sent

def AddAttachment(date_sent, senderid, attachment):
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT message_id FROM Message
                            WHERE sender_id = :senderid AND
                            date_time_sent = :date_sent""",
                        {"date_sent" : date_sent, "senderid" : senderid}
                        )
        for r in cur:
            message_id = r[0]
            
        c.execute("""INSERT INTO Attachment (message_id, file)
                    VALUES (:message_id, :attachment);""",
                      {"message_id": message_id, "attachment": attachment})
					  
			
			
def Send_Message(date_sent, senderid, recipientid):
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT message_id FROM Message
                            WHERE sender_id = :senderid AND
                            date_time_sent = :date_sent""",
                        {"date_sent" : date_sent, "senderid" : senderid}
                        )
        for r in cur:
            a = r[0]
    
        c.execute("""INSERT INTO Receiving (recipient_id, date_time_received,
                        is_received, message_id)
                        VALUES (:recipient_id, :date_time_received,
                        :is_received, :message_id)""",
                      {"recipient_id" : recipientid, "date_time_received" : "",
                      "is_received" : 'n', "message_id" : a})



def Save_Draft(date_sent, senderid):
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT message_id FROM Message
                            WHERE sender_id = :senderid AND
                            date_time_sent = :date_sent""",
                        {"date_sent" : date_sent, "senderid" : senderid}
                        )
        for r in cur:
            a = r[0]
    
        c.execute("""INSERT INTO Receiving (recipient_id, date_time_received,
                        is_received, message_id)
                        VALUES (:recipient_id, :date_time_received,
                        :is_received, :message_id)""",
                      {"recipient_id" : "", "date_time_received" : "",
                      "is_received" : 'n', "message_id" : a})

        
def Conversation(userid1, userid2):
    apot=[]
    with conn:
        
        #Getting name and last name for userid1
        c = conn.cursor()
        cur = c.execute("""SELECT first_name, last_name FROM User
                        WHERE user_id=:userid""",\
                            {"userid" : userid1})

        for r in cur:
            name1 = r[0]
            lastname1 = r[1]

        #Getting name and last name for userid2
        cur = c.execute("""SELECT first_name, last_name FROM User
                        WHERE user_id=:userid""",\
                            {"userid" : userid2})

        for r in cur:
            name2 = r[0]
            lastname2 = r[1]

        #Getting alla messages between the two users
        cur = c.execute("""SELECT sender_id, recipient_id, message_body, date_time_sent
                FROM (Message JOIN Receiving ON Message.message_id = Receiving.message_id)
            WHERE ( (sender_id=:u1 AND recipient_id=:u2) OR (sender_id = :u2 AND recipient_id=:u1) )
            ORDER BY date_time_sent ASC""", {"u1":userid1, "u2":userid2, "u1":userid1, "u2":userid2})
        
        for r in cur:
            apot.append(r)

        #Printing all messages with the right format

        for r in apot:
            if (r[0] == userid1):
                print (name1, lastname1, end="")
                print(":", r[2], "|Sent at: ", end="")
                for i in range(16):
                    print(r[3][i], end="")
                print()
            else:
                print (name2, lastname2, end="")
                print(":", r[2], "|Sent at: ", end="")
                for i in range(16):
                    print(r[3][i], end="")
                print()


def See_Drafts(userid1):
    with conn:
        c = conn.cursor()

        #Getting name and last name for user
        cur = c.execute("""SELECT first_name, last_name FROM User
                        WHERE user_id=:userid""",\
                            {"userid" : userid1})

        for r in cur:
            name1 = r[0]
            lastname1 = r[1]
        
        cur = c.execute("""SELECT message_body, date_time_sent
                FROM (Message JOIN Receiving ON Message.message_id = Receiving.message_id)
            WHERE ( (sender_id=:u1 AND recipient_id=:u2) OR (sender_id = :u2 AND recipient_id=:u1) )
            ORDER BY date_time_sent ASC""", {"u1":userid1, "u2": "", "u1":userid1, "u2": ""})
        k=1
        for r in cur:
            print (k, ':', r[0],end = " ")
            for i in range(16):
                print(r[1][i], end="")
            print()
            k = k + 1
            

def Check_My_Stats(userid):
    apot = []
    with conn:
        c = conn.cursor()
        cur = c.execute("""SELECT * FROM User
                            WHERE user_id=:userid""",\
                            {"userid" : userid})
        for r in cur:
            for i in range(9):
                apot.append(r[i])

        print ("User ID:", apot[0])
        print ("First Name:", apot[1])
        print ("Last Name:", apot[2])
        print ("Avatar:", apot[3])
        print ("Phone Number:", apot[4])
        print ("E-mail:", apot[5])
        print ("User since:", apot[7])
        if (apot[8]=='y'):
            print ("Status: Active")
        else:
            print ("Status: Inactive")
			
			
def Update_Account(userid):
    ##allows end user to change name, avatar, phone, email and password
    a = -1
    with conn:
        c = conn.cursor()
        while (a not in range(7)):
            print ("\n1) Email")
            print ("2) Password")
            print ("3) Name")
            print ("4) Last Name")
            print ("5) Avatar")
            print ("6) Phone")
            print ("0) Go Back")
            print ("What would you like to do: ", end='')
            a = int(input())
            if (a==1):
                cur = c.execute("""SELECT e_mail FROM User
                                WHERE user_id = :userid""", \
                                  {"userid" : userid})
                for r in cur:
                    print ("Old email:", r[0])
                print ("New email: ", end='')
                email = input()
                c.execute("""UPDATE User SET e_mail = :email
                            WHERE user_id = :userid""", \
                          {"email" : email, "userid" : userid})
            elif (a==2):
                
                #------------Password hashing---------------
                while (True):
                    #print ("Password: ", end='')
                    raw_password = getpass.getpass("New password: ")
                    #print ("Password confirmation: ", end="")
                    raw_password2 = getpass.getpass("New password confirmation: ")
                    if (raw_password == raw_password2):
                        break
                    print ("Password mismatch, try again!")
                salt = hashlib.sha256(str(random.getrandbits(512)).encode('utf-8')).hexdigest()[:5]
                hsh = hashlib.sha256(('%s%s' % (salt, raw_password)).encode('utf-8')).hexdigest()
                final_password = '%s$%s' % (salt, hsh)
            
                #-----------------------------------------
                
                c.execute("""UPDATE User SET password = :password
                            WHERE user_id = :userid""", \
                          {"password" : final_password, "userid" : userid})
            elif (a==3):
                cur = c.execute("""SELECT first_name FROM User
                                WHERE user_id = :userid""", \
                                  {"userid" : userid})
                for r in cur:
                    print ("Old name:", r[0])
                print ("New name: ", end='')
                name = input()
                c.execute("""UPDATE User SET first_name = :name
                            WHERE user_id = :userid""", \
                          {"name" : name, "userid" : userid})
            elif (a==4):
                cur = c.execute("""SELECT last_name FROM User
                                WHERE user_id = :userid""", \
                                  {"userid" : userid})
                for r in cur:
                    print ("Old last name:", r[0])
                print ("New last Name: ", end='')
                lastname = input()
                c.execute("""UPDATE User SET last_name = :lastname
                            WHERE user_id = :userid""", \
                          {"lastname" : lastname, "userid" : userid})
            elif (a==5):
                cur = c.execute("""SELECT avatar FROM User
                                WHERE user_id = :userid""", \
                                  {"userid" : userid})
                for r in cur:
                    print ("Old avatar:", r[0])
                print ("New avatar: ", end='')
                avatar = input()
                c.execute("""UPDATE User SET avatar = :avatar
                            WHERE user_id = :userid""", \
                          {"avatar" : avatar, "userid" : userid})
            elif (a==6):
                cur = c.execute("""SELECT phone_number FROM User
                                WHERE user_id = :userid""", \
                                  {"userid" : userid})
                for r in cur:
                    print ("Old phone:", r[0])
                print ("New phone: ", end='')
                phone = input()
                c.execute("""UPDATE User SET phone_number = :phone
                            WHERE user_id = :userid""", \
                          {"phone" : phone, "userid" : userid})
            else:
                  pass

            if (a):
                print ("")
                print ("Profile updated successfully!")
                print ("Press anything to continue.")
                wait = input()


def Logout(userid):
    with conn:
        c = conn.cursor()
        c.execute("""UPDATE User SET is_active = 'n'
                        WHERE user_id = :userid""", \
                      {"userid" : userid})

    
def DB_Admin():
    conn = sqlite3.connect("vibegram.db")
    c = conn.cursor()
    print("To go back, type Back")
    query = input("Enter your SQL query: ")
    while(query!="Back"):
        try:
            c.execute(query)
            results = c.fetchall()
            print(results)
            conn.commit()
            
        except sqlite3.OperationalError as e:
            ##print('er:', e.__traceback__)
            print("SQL Error, please try again")
        query = input("Enter your SQL query: ")
