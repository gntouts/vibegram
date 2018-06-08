import sqlite3
import datetime as dt
from dbclass import *
from DBHandling import *
from UserFunctions import *


def WelcomeMenu():
    a = -1
    while (a not in range(3)):
        print ("1) Sign In")
        print ("2) Sign Up")
        print ("0) Exit program")
        print ("What would you like to do: ", end='')
        a = int(input())
    return a

def WelcomeAction(choice, c):

    if (choice == 1):
        return Sign_In(c)
    if (choice == 2):
        return Create_Acc(c)
    else:
        pass
            
def MainMenu(userid, c):
    cur = c.execute("SELECT first_name, last_name FROM Users WHERE user_id = ?", (userid,))
    for r in cur:
        name = r[0]
        lastname = r[1]
    print ("\nHello", name, lastname, "!")

    print ("1) Search users and add them as Friends")
    print ("2) See Friends")
    print ("3) Update Profile")
    print ("4) Send message to a user") 
    print ("0) Exit")
    print ("What would you like to do: ", end='')
    return int(input())

def MainAction(choice,userid, c):
    if (choice == 1):
        results=[]
        results = Search_Users(c)
        #print (results)
        print ("Chose a user to be added to your Friends or press 0 to go back")
        a = int(input())
        Add_Friend(a, userid, results[a][0], c, "")
    if (choice == 2):
        Contact_List(userid, c)
        print ("\nPress enter to continue")
        wait = input()
    if (choice==3):
        Update_Account(userid, c)
    if (choice==4):
        Contact_List(userid, c)
        print ("Select a User by his user ID to send him a message: ")
        userid2 = int(input())
        Create_Mess(userid, userid2, c)
        
        

        
def main():
    conn = sqlite3.connect('vibegram.db')
    c = conn.cursor()

    #gia arxh meta tha to bgaloume
    print ("Creating database...")
    CreateTables(c)
    print ("Done!")

    choice = WelcomeMenu()
    userid = WelcomeAction(choice, c)
    while (choice != 0):
        choice = MainMenu(userid, c)
        MainAction(choice, userid, c)
    print ("Closing...")
    conn.commit()
    conn.close
    
if __name__ == "__main__":
    main()
