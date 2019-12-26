from tkinter import *
import os, hashlib


def verify():
    func = lambda: account.set("Selected Account: None")
    func2 = lambda: account.set(F"Selected Account: {userName}")

    account.set("Verifying credentials...")

    with open("users.txt",'r') as file:
        userNames = file.readlines()
    with open("passwords.txt", 'r') as file:
        passWords = file.readlines()
    
    userName = user.get()
    passWord = password.get()

    eUserName = hashlib.sha384(userName.encode('UTF-8'))
    ePassWord = hashlib.sha384(passWord.encode('UTF-8'))

    eUserName = eUserName.hexdigest()
    ePassWord = ePassWord.hexdigest()

    for a, b in zip(userNames, passWords):
        if F"{eUserName}\n" == a and F"{ePassWord}\n" == b:
            account.set("Access Granted!")
            root.after(2000, func2)
            return None

    account.set("Access Denied!")
    root.after(2000, func)


def signingUp():
    global account

    func = lambda: account.set("Selected Account: None")

    userName = user.get()
    passWord = password.get()
    
    if userName == None or userName == "":
        account.set("Username cannot be blank!")
        root.after(2000, func)
        return None

    elif passWord == None or passWord == "" or len(passWord) < 8:
        account.set("Password must be at least 8 characters!")
        root.after(2000, func)
        return None
        
    else:
        eUserName = hashlib.sha384(userName.encode('UTF-8'))
        ePassWord = hashlib.sha384(passWord.encode('UTF-8'))

        eUserName = eUserName.hexdigest()
        ePassWord = ePassWord.hexdigest()

        with open("users.txt", 'a') as file:
            file.write(F"{eUserName}\n")
        
        with open("passwords.txt", 'a') as file:
            file.write(F"{ePassWord}\n")


if __name__ == "__main__":
    if not os.path.isfile("passwords.txt"):
        file = open("passwords.txt", "w+")
        file.close()
    if not os.path.isfile("users.txt"):
        file = open("users.txt", "w+")
        file.close()

    root = Tk()

    frame = Frame(root)
    frame.pack()

    user = Entry(frame)
    user.grid(row=0)

    password = Entry(frame)
    password.grid(row=1)

    logIn = Button(frame, text="Log In", command=verify)
    logIn.grid(row=0, rowspan=2, column=1)

    signUp = Button(frame, text="Sign Up", command=signingUp)
    signUp.grid(row=0, rowspan=2, column=2)

    account=StringVar()
    account.set("Selected Account: None")
    selectedAccount = Label(frame, textvariable=account)
    selectedAccount.grid(row=2, columnspan=3)

    root.mainloop()