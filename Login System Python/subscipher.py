import sqlite3
import re
import sys


def encrypt(txt):
    x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    y = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    table = str.maketrans(x, y)
    transl = txt.translate(table)
    return transl


def decrypt(txt):
    x = 'TIMEODANSFRBCGHJKLPQUVWXYZtimeodansfrbcghjklpquvwxyz9876543210'
    y = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    table = str.maketrans(x, y)
    transl = txt.translate(table)
    return transl


def db_check():
    conn = sqlite3.connect("loginsys.db", timeout=1)
    c = conn.cursor()
    try:
        c.execute("UPDATE user SET ACCESS_COUNT = ACCESS_COUNT + 1 WHERE LOGIN =?", ['admin'])
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(e)
        print("Database might be locked check and run again")
        sys.exit()


def tbcreator():
    conn = sqlite3.connect("loginsys.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE user
        		("USER_ID"	INTEGER NOT NULL,
    	"LOGIN"	TEXT NOT NULL UNIQUE,
    	"CRYPT_PASS"	TEXT NOT NULL,
    	"ACCESS_COUNT"	INTEGER NOT NULL,
    	PRIMARY KEY("USER_ID" AUTOINCREMENT))''')
    c.execute("INSERT INTO user(LOGIN, CRYPT_PASS, ACCESS_COUNT) VALUES ('admin', 'tecsg', '0' )")
    conn.commit()
    conn.close()


def remove(string):
    unamestrip = string.replace(" ", "")
    return unamestrip


def check_pass(pwd):
    pattern = "^[A-Za-z0-9]*$"
    while not re.match(pattern, pwd):
        pwd = input("Enter account password to add (letters and numbers only): ")
    else:
        pass
    return pwd


def check_email(uname):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    while not re.fullmatch(regex, uname):
        uname = input("Invalid email please check entry Enter account email to add: ")

    else:
        pass
    return uname


def backup():
    try:
        conn = sqlite3.connect("loginsys.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user")
        results = c.fetchall()
        headers = [i[0] for i in c.description]
        import csv

        csvfile = csv.writer(open('userbckup.csv', 'w', newline=''),
                             delimiter=',', lineterminator='\r\n',
                             quoting=csv.QUOTE_ALL, escapechar='\\')
        csvfile.writerow(headers)
        csvfile.writerows(results)
        print("backup success")
        conn.close()
    except sqlite3.DatabaseError as e:
        print(e)
        print("backup unsuccessful")
    except PermissionError as w:
        print(w)
        print("backup unsuccessful")
        print("Check if the file is already open")
