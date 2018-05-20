import sqlite3
import datetime as dt
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

    if (choice == 1):
        return Sign_In()
    if (choice == 2):
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
            
def MainMenu(userid, c):
    cur = c.execute("SELECT first_name, last_name FROM Users WHERE user_id = ?", (userid,))
    for r in cur:
        name = r[0]
        lastname = r[1]
    print ("Hello", name, lastname, "!")

    #gia pes gnwmh gia edw...mallon den ftanei ena kentriko interface
    print ("Choose one of the following:")
    print ("1) See contacts")
    print ("2) Create message")
    print ("0) Exit")

        
def main():
    conn = sqlite3.connect('vibegram.db')
    c = conn.cursor()

    #gia arxh meta tha to bgaloume
    print ("Creating database...")
    CreateTables(c)
    print ("Done!")

    choice = WelcomeMenu()
    userid = WelcomeAction(choice, c)
    choice = MainMenu(userid, c)

    print ("Closing...")
    conn.commit()
    conn.close
if __name__ == "__main__":
    main()
