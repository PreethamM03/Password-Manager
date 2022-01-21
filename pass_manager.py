import sqlite3, hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial

from sqlalchemy import column


#Database Setup
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS manager(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")


#PopUps
def popUp(input):
    answer = simpledialog.askstring("Input string", input)

    return answer



#Creates Window
window = Tk()

window.title("Password Manager")



def hashPassword(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash
def entryScreen():
    window.geometry("350x150")

    lbl = Label(window, text = "Create Master Password")
    lbl.config(anchor = CENTER)
    lbl.pack()

    txt = Entry(window, width = 20, show='*')
    txt.pack() 
    txt.focus()

    lbl1 = Label(window, text='Re-enter Password')
    lbl1.pack()

    txt1 = Entry(window, width = 20, show='*')
    txt1.pack() 

    lbl2 = Label(window)
    lbl2.pack()

    
    def savePassword():
        if txt.get() == txt1.get():
            hashedPassword = hashPassword(txt.get().encode('utf-8'))
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            manager()
        else:
            lbl2.config(text="Passwords do not match")

    btn = Button(window, text = "submit", command = savePassword)
    btn.pack()
def login():
    window.geometry("350x150")

    lbl = Label(window, text = "Enter Master Password")
    lbl.config(anchor = CENTER)
    lbl.pack()

    txt = Entry(window, width = 20, show='*')
    txt.pack() 
    txt.focus()

    lbl1 = Label(window)
    lbl1.pack()

    def getMastPwd():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))

        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()
    def checkPassword():
        pwd = getMastPwd()

        if pwd:
            manager()
        else:
            txt.delete(0, "end")
            lbl1.config(text="Incorrect Password")
    btn = Button(window, text = "submit", command = checkPassword)
    btn.pack()

def manager():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry("750x350")

    def addEntry():
        prompt1 = 'Website'
        prompt2 = 'Username'
        prompt3 = 'Password'

        website = popUp(prompt1)
        username = popUp(prompt2)
        password = popUp(prompt3)

        insertFields = """INSERT INTO manager(website,username,password)
        VALUES(?,?,?)"""

        cursor.execute(insertFields, (website, username, password))
        db.commit()

        manager()
    
    def removeEntry(input):
        cursor.execute("DELETE FROM manager WHERE id = ?", (input,))
        db.commit()

        manager()

    lbl = Label(window, text = "Add Account")
    lbl.grid(column=1)
    
    btn = Button(window, text= '+', command = addEntry)

    btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=80)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM manager")
    if(cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM manager")
            array = cursor.fetchall() 

            lbl1 = Label(window, text=(array[i][1]), font=('Helvetica', 12))
            lbl1.grid(column=0, row= i+3)


            lbl1 = Label(window, text=(array[i][2]), font=('Helvetica', 12))
            lbl1.grid(column=1, row= i+3)


            lbl1 = Label(window, text=(array[i][3]), font=('Helvetica', 12))
            lbl1.grid(column=2, row= i+3)

            btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
            btn.grid(column=3, row =i+3, pady=10)
            i = i+1

            cursor.execute("SELECT * FROM manager")
            if(len(cursor.fetchall()) <= i):
                break
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    login()
else:
    entryScreen()
window.mainloop()