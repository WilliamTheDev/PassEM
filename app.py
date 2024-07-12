import json

from scripts import crypt 
from scripts import database
from getpass import getpass

# global variables
dataBasePath = './database/accounts.json'

def add_account(account: dict, master: str) -> None:
    # reads database & gets the number of accounts
    data = database.read(dataBasePath)
    numAccount = len(data['accounts']) + 1
    # encrypts the account data & deletes the unencrypted data
    encryptedAccount = crypt.encrypt(str(account), master)
    del account

    # Writes the encrypted data 
    data['accounts'][numAccount] = encryptedAccount
    database.write(dataBasePath, data)


def show_accounts() -> None:
    # reads database
    data = database.read(dataBasePath)
    for account in data['accounts']:
        decrypt = (crypt.decrypt(data['accounts'][account], master))
        accountDecode = decrypt.decode('utf-8')  
        account = json.loads(accountDecode.replace("'", '"'))  
        print(account['name'], account['label'], account['password'])
        
master = getpass("enter master password: ")
#add_account(account, master)
show_accounts()
