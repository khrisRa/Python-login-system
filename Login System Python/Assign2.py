import sqlite3
import os
import subscipher
import time

if os.path.exists("loginsys.db"):
    subscipher.db_check()
else:
    subscipher.tbcreator()

while True:
    print("""
        1. if you want to Sign Up
        2. if you want to Login 
        3. if you want to Exit and Backup
    """)
    accOrLog = input("Please enter your choice: ")

    if accOrLog == "1":
        fieldstrip = subscipher.remove(input("Enter account email to add: "))
        uname = subscipher.check_email(fieldstrip)
        pwd = subscipher.check_pass(input("Enter account password to add (letters and numbers only): "))
        encrypted = subscipher.encrypt(pwd)
        access = '0'
        conn = sqlite3.connect("loginsys.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE LOGIN=?", [uname])

        if c.fetchone():
            print("Username already exists, please try again with different username")
        else:
            c.execute("INSERT INTO user(LOGIN, CRYPT_PASS, ACCESS_COUNT) VALUES (?, ?, ?)", [uname, encrypted, access])
            conn.commit()
            conn.close()
            print("Account added")
    elif accOrLog == "2":
        uname = subscipher.remove(input("Enter username: "))
        pwd = input("Enter password: ")
        encrypted = subscipher.encrypt(pwd)
        conn = sqlite3.connect("loginsys.db")
        c = conn.cursor()

        c.execute("SELECT * FROM user WHERE LOGIN=? and CRYPT_PASS=?", [uname, encrypted])

        if c.fetchone() is None:
            print("Incorrect credentials, please verify username and password and try again")
        else:
            c.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", [uname])
            c.execute("SELECT * FROM user WHERE LOGIN=?", [uname])
            record = c.fetchall()
            for row in record:
                print("Access Count: ", row[3])
                conn.commit()
                conn.close()
            print("Logged in!")

    elif accOrLog == "3":
        subscipher.backup()
        print("Good Bye closing in 5secs")
        time.sleep(5)
        break
    else:
        print("You have to press 1 or 2 or 3")
