import hashlib
import sys

def sha512r(myStr, n = 10000):
    '''Recursive sha512 takes feeds the output of sha512 back into sha512 n times making it more iterative than recursive
    When n == 10000, it takes 10000 times longer than sha512 making it more difficult to brute force via a list of possible passwords'''
#    if n:  # true recursive approach but limited by max depth
#        return hashlib.sha512(sha512r(myStr, n-1).encode()).hexdigest()
#    return 
#        return hashlib.sha512(myStr.encode()).hexdigest()
    for _ in range(n):
        myStr = hashlib.sha512(myStr.encode()).hexdigest()
    return myStr

class Users():
    'An object that tracks user\'s names and a hash of their password'

    def __init__(self, userHashes = {}):
        'Initilizes the only member variable, a dictionary. It has a key for every username and it\'s value is the associated password\'s hash by use of sha512r (my defined recursive hash function)'
        self.userHashes = userHashes

    def addUsr(self, userName, passWord):
        'adds user userName to the database with the hash of passWord if userName is not already taken.'
        if userName in self.userHashes:
            print(f'Sorry, {userName} is already taken')
            return
        self.userHashes[userName] = sha512r(passWord)
        print('User successfully added')

    def login(self, userName, passWord):
        'Login prints login success if the password is correct, incorrect password if it is not, and incorrect user name if that userName is not in the database'
        if userName in self.userHashes:
            if self.userHashes[userName] == sha512r(passWord):
                print('Login Success')
            else:
                print('Incorrect Password')
        else:
            print('Incorrect User Name')

    def changePassword(self, userName, passWord, newPassWord):
        'Changes the hash associated with userName to that of newPassWord if the hash from passWord matches the hash saved for userName in the database'
        if userName in self.userHashes:
            if self.userHashes[userName] == sha512r(passWord):
                self.userHashes[userName] = sha512r(newPassWord)
                print('Password successfully updated')
            else:
                print('That is not your current password')
        else:
            print('That user does not exist')

    def listHashTable(self):
        'This clearly prints out user names and associated hashes of their passwords'
        for key, value in self.userHashes.items():
            print(f'{key}\'s password has hash:\n{value}')

    def removeUser(self, username, password):
        'Removes username and it\'s associated password\'s hash if the hash of password matches it'
        if username not in self.userHashes:
            print(f'{username} is not a valid user name')
            return
        if username in self.userHashes:
            if self.userHashes[username] == sha512r(password):
                self.userHashes.pop(username)
                print(f'You have successfully removed {username}\'s account')
            else:
                print('Incorrect Password')
        else:
            print('Incorrect User Name')

def ls(H):
    'used to call listHashTable method from ui'
    H.listHashTable()

def login(H):
    'used to call login method from ui and is somewhat rhobust requring some input for user and password'
    user = password = ''
    while not user:
        user = input('Enter your username:\t').capitalize()
    while not password:
        password = input('Enter your password:\t')
    H.login(user, password)

def cp(H):
    'used to call changePassword method from ui and is somewhat rhobust requring some input for user, password and noePassword'
    user = password = newPassword = ''
    while not user:
        user = input('Enter your username:\t')
    while not password:
        password = input('Enter your password:\t')
    while not newPassword:
        newPassword = input('Enter your password:\t')
    H.changePassword(user, password, newPassword)

def add(H):
    'used to call addUsr method from ui and is somewhat rhobust requring some input for user and password'
    user = password = ''
    while (not user) or (len(user.split()) > 1):
        user = input('Enter your username (no spaces):\t').capitalize()
    while not password:
        password = input('Enter your password:\t')
    H.addUsr(user, password)

def remove(H):
    'used to call removeUser method from ui and is somewhat rhobust requring some input for user and password'
    user = password = ''
    while (not user) or (len(user.split()) > 1):
        user = input('Enter your username (no spaces):\t').capitalize()
    while not password:
        password = input('Enter your password:\t')
    H.removeUser(user, password)

def ui():
    'a simple command line interface to work with a Users class loading data from a text file and updating that file with any changes made'
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    else:
        fileName = 'hashList.txt'
    user = password = UI = ''
    myDict = {}
    try:
        myFile = open(fileName, 'r')
        i = 0
        elems = myFile.read().split()
        for elem in elems:
            i+=1
            if i % 2 == 1:
                lastLine = elem
            else:
                myDict[lastLine] = elem
        if i < 2:
            raise(f'The file {fileName} is empty')
        myFile.close()
    except:
        UI = ''
        while not (UI.lower().startswith('y') or UI.lower().startswith('n')):
            UI = input('Would you like to add a user?(y\\n):\t')
        while UI.lower().startswith('y'):
            UI = ''
            while not user or len(user.split()) > 1:
                user = input('Enter your username (no spaces):\t').capitalize()
            while not password:
                password = input(f'What is {user}\'s password?\t')
            if user not in myDict:
                myDict[user] = sha512r(password)
            else:
                print(f'The username {user} is already taken')
            while not (UI.lower().startswith('y') or UI.lower().startswith('n')):
                UI = input('Would you like to add a user?(y\\n):\t')
            user = password = ''
    H = Users(myDict)
    commands = {
            'ls' : ls,
            'login' : login,
            'cp': cp,
            'add' : add,
            'remove' : remove
            }
    print(16*'*'+'\nAvailable Commands:\nls (List Hash Table)\nlogin\ncp (Change Password)\nadd (Add New User)\nexit\nquit (don\'t save)\n'+16*'*')
    UI = input('>>>\t')
    while not UI:
        UI = input('>>>\t')
    while UI.lower() not in ('exit', 'quit'):
        if UI.lower().split()[0] in commands:
            commands[UI.lower().split()[0]](H)
        else:
            print(f'\"{UI}\" is not a valid command')
        UI = input('>>>\t')
#    if H.userHashes: # uncomment this and indent the following four lines to disable destruction of the database if all users were removed 
    if UI.lower() != 'quit':
        myFile = open(fileName, 'w')
        for userElem, hashElem in H.userHashes.items():
            myFile.write(f'{userElem} {hashElem} ')
        myFile.close()
        print('Have a great day!')
    else:
        print('Changes not saved')

ui()

