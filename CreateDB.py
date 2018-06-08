import sqlite3
import datetime as dt
import names, random
from DML import *

def CreateTables():

    conn = sqlite3.connect('vibegram.db')
    c = conn.cursor()
    
    #Allagh apo Users se User
    c.execute("""CREATE TABLE IF NOT EXISTS User (
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
    #Allagh apo Messages se Message                
    c.execute("""CREATE TABLE IF NOT EXISTS Message (
                         message_id integer PRIMARY KEY AUTOINCREMENT,
                         sender_id integer,
                         is_sent varchar,
                         date_time_sent datetime,
                         message_body text                         
                         );
                         """)
                        
    c.execute("""CREATE TABLE IF NOT EXISTS Receiving (			
                         recipient_id integer,
                         date_time_received datetime,
                         is_received varchar,
                         message_id integer
                         );
                         """)
                                                     
    c.execute("""CREATE TABLE IF NOT EXISTS Attachment(			
                                                    message_id integer,
                                                    file blob
                         );
                         """)
                                                     
    conn.commit()
    conn.close()

def PopulateDB():

    conn = sqlite3.connect('vibegram.db')
    c = conn.cursor()

    #------------------Create Users-------------------
    
    for i in range(1000):
        #---------------Create dummy data---------------
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = first_name[0]+"."+last_name+str(random.randint(1, 99))+"@gmail.com"
        phone = int("69" + str(random.randint(10000000, 99999999)))

        #---------------Insert User--------------------------
        Ins_User(first_name, last_name, "", phone, \
                 email, "pass", dt.datetime.now(), 'n' )
    
    
                        
    conn.commit()
    conn.close()
