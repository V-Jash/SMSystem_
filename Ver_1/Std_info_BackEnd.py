import os
import sqlite3
BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'student.db')


def connect():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    roll TEXT UNIQUE,
                    dob TEXT,
                    contact TEXT
                    email TEXT,
                    gender TEXT,
                    class_ TEXT,
                    address TEXT)""")


def insert(name, roll, dob, contact, email, gender, class_, address):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(""" INSERT INTO students (name,roll,dob,contact,email,gender,class_,address)
                        VALUES(?,?,?,?,?,?,?,?)
    """, (name, roll, dob, contact, email, gender, class_, address))
            return cur.lastrowid
        except sqlite3.IntegrityError:
            return None


def view():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        return cur.fetchall()


def search(name="", roll="", dob="", contact="", email="", gender="", class_="", address=""):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM students WHERE name IS LIKE ?,
                    roll IS LIKE ?,
                    dob IS LIKE ?,
                    contact IS LIKE ?,
                    email IS LIKE ?,
                    gender IS LIKE ?,
                    class_ IS LIKE ?,
                    address IS LIKE ?

""", (f"%{name}%", f"%{roll}%", f"%{email}%", f"%{gender}%",
            f"%{class_}%", f"%{contact}%", f"%{dob}%", f"%{address}%"))
        return cur.fetchall()


def update(id, name, roll, dob, contact, email, gender, class_, address):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute(
            """UPDATE students SET name=?,roll=?,dob=?,contact=?,email=?,gender=?,class_=?,address=? WHERE id = ?""", (id,))
        cur.rowcount


def delete(id):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute(""" DELETE FROM students WHERE id=?""", (id,))
        cur.rowcount


connect()
