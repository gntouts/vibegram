import sqlite3
import datetime
from dbclass import *
from DBHandling import *


def WelcomeMenu():
    a = -1
    while (a not in range(3)):
        print ("Choose one of the following:")
        print ("1) Sign In")
        print ("2) Sign Up")
        print ("0) Exit program")
        a = int(input())
    return a

def WelcomeAction(choice, c):

    if (choice==1):
        found = 0
        while (found):
            email = input("Email: ")
            password = input("Password: ")
            cur = c.execute("SELECT user_id FROM Users WHERE e_mail = :email AND password = :password", {"email":email, "password":password})
            for r in cur:
                found = r[0]
            if (not found):
                print ("Wrong username or password, try again!")


def MainMenu():
    pass
            
def main():
    conn = sqlite3.connect('vibegram.db')
    c = conn.cursor()

    #gia arxh meta tha to bgaloume
    print ("Creating database...")
    CreateTables(c)
    print ("Done!")

    choice = WelcomeMenu()
    WelcomeAction(choice, c)
    print("Welcome to Vibegram")
    choice = MainMenu()
    

if __name__ = "__main__":
    main()
