import sqlite3
import datetime as dt
import getpass as gp
from CreateDB import *
from DML import *


def WelcomeMenu():
    a = -1
    while (a not in range(4)):
        cls()
        print ("1) Sign In")
        print ("2) Sign Up")
        print ("0) Exit program")
        print ("What would you like to do: ", end='')
        try:
            a = int(input())
        except ValueError as e:
            pass
    return a

	
def WelcomeAction(choice):

    if (choice == 1):
        cls()
        return Sign_In()
    if (choice == 2):
        print('hi new user')
        cls()
        return Create_Acc()
    if (choice == 3):

        key = input("Enter key: ")
        if (key == "root"):
            cls()
            DB_Admin()
            return -0
        else:
            return 0
    else:
        return -1



def MainMenu(userid):
    
    c = conn.cursor()
    a=-1
    while (a not in range(8)):
        cls()
        cur = c.execute("SELECT first_name, last_name FROM User WHERE user_id = ?", (userid,))
        for r in cur:
            name = r[0]
            lastname = r[1]
        print ("\nHello", name, lastname, "!")
        print ("1) Search users and add them as Friends")
        print ("2) See Friends")
        print ("3) Send message to a user")
        print ("4) Open conversation")
        print ("5) See draft messages")
        print ("6) Check my profile")
        print ("7) Update Profile")
        print ("0) Logout")
        print ("What would you like to do: ", end='')
        try:
            a = int(input())
        except ValueError as e:
            cls()        
    return a

def MainMenuAction(choice, userid):
    results=[]
    cls()
    if (choice == 1):
	
        results = Search_Users()
        if (results != []):
            print ("Choose a user to be added to your Friends or press 0 to go back")
            a = int(input())
            if (a):
                print ("Choose type of friend: ", end="")
                tupos = input()
                Add_Friend(a, userid, results[a][0], tupos)
                c = conn.cursor()
                cur = c.execute("SELECT first_name, last_name FROM User WHERE user_id = ?", (results[a][0],))
                for r in cur:
                    name = r[0]
                    lastname = r[1]
                print ("Congratulations you are now friend with", r[0], r[1], "!" )
        return userid
    
    elif (choice == 2):

        #-----------Print all users that you are friends with-----------
        results = Contact_List(userid)
        print ("\nPress enter to continue ", end="")
        wait = input()
        return userid
    
    elif (choice==3):
        
        #----------Enter Message body--------------
        print("Enter the text of your message or press enter to go back")
        body = input()
        if (not body):
            return userid
        timestamp = Create_Message(body, userid)

        
        #-----------Enter attachment if any---------
        a = ""
        while (a!="y" and a!="n"):
            print ("Do you want to attach any file? (y/n)")
            a = input()
        if (a=="y"):
            print ("Attachment: ")
            attachment = input()
            AddAttachment(timestamp, userid, attachment)

        #-----------Enter recipient-----------------
        print("Select desired recipient: ", end = "")
        results = Contact_List(userid)
        print ("0 ) Save as draft")
        userid2 = int(input())
        if (userid2):
            Send_Message(timestamp, userid, results[userid2])
            print("Message sent!")
        else:
            Save_Draft(timestamp, userid)
            print ("Message saved as draft!")
        
        return userid
    
    elif (choice==4):

        #---------Select friend and print conversation---------------
        print("Select a friend to see your conversation: ", end = "")
        results = Contact_List(userid)
        print ("0) Go Back")
        userid2 = int(input())
        if (not userid2):
            return userid
        
        Conversation(userid, results[userid2])
        
        print ("\nPress enter to continue ", end="")
        wait = input()
        return userid

    elif (choice==5):

        print ("--------Drafts--------")
        See_Drafts(userid)

        print ("\nPress enter to continue ", end="")
        wait = input()
        
        return userid

        
    elif (choice==6):
        
        print ("")
        print ("------Profile Information------")
        Check_My_Stats(userid)
        print ("\nPress enter to continue ", end="")
        wait = input()
        return userid
    
    elif (choice==7):
    
        Update_Account(userid)
        return userid
    
    elif (choice==0):
        
        print("Logging out...\n")
        Logout(userid)
        userid = 0
        return userid
        
        

		
def main():
    conn = sqlite3.connect('vibegram.db')

    #gia arxh meta tha to bgaloume
    print ("Creating database...")
    CreateTables()
    print ("Done!")
    a = ""
    while (a!="y" and a!="n"):
        print ("Do you want to populate the Database? (1000 new users) (y/n)")
        a = input()
    if (a=="y"):
        print ("Populating Database...")
        PopulateDB()
        print ("Done!")

    exit_flag = 0
    while(exit_flag == 0):
        choice = WelcomeMenu()
        userid = WelcomeAction(choice)
        if (userid == -1):
              exit_flag = 1
              logout_flag = 1
        elif (userid == 0):
            logout_flag = 1
        else:
            logout_flag = 0
        

        
        while (logout_flag == 0):
            choice = MainMenu(userid)
            userid = MainMenuAction(choice, userid)
            if (userid != 0):
                logout_flag = 0
            else:
                logout_flag = 1


        
    print ("Closing...")
    conn.commit()
    conn.close
    
if __name__ == "__main__":
    main()
