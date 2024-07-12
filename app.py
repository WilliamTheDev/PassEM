import json

from scripts import crypt 
from scripts import database
from getpass import getpass

# global variables
DBPATH = './database/accounts.json'

def create_account() -> dict:
    # Creates and fills a new account  
    newAccount = {}
    newAccount['name'] = input("Enter the new service name: ")
    newAccount['label'] = input("Enter a label name: ")
    newAccount['password'] = getpass("Enter the service password: ")
    return newAccount

# adds a new account to DB
def add_account(newAccount: dict, masterPass: str) -> None:
    # reads database & gets the number of accounts
    dbData = database.read(DBPATH)
    accountID = len(dbData['accounts']) + 1
    # encrypts the account data & deletes the unencrypted data
    encryptedData = crypt.encrypt(str(newAccount), masterPass)
    del newAccount
 
    # Writes the encrypted data 
    dbData['accounts'][accountID] = encryptedData
    database.write(DBPATH, dbData)

# Shows all accounts
def show_accounts(masterPass) -> None:
    # reads database
    dbData = database.read(DBPATH)
    if len(dbData['accounts']) < 0:  
        print("the database is empty")
        return 

    #Decrypts the account and prints it 
    for account in dbData['accounts']:
        accountDecrypted = crypt.decrypt(dbData['accounts'][account], masterPass)
        accountDecode = accountDecrypted.decode('utf-8')  
        account = json.loads(accountDecode.replace("'", '"'))  
        print(account['name'], account['label'], account['password'])

masterPass = input("Enter the master password: ")
show_accounts(masterPass)
add_account(create_account(), masterPass)
show_accounts(masterPass)
