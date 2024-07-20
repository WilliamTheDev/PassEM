
from scripts import database as data_base
from scripts import crypt

from random import choice 
from string import digits, ascii_letters, punctuation
from getpass import getpass
from prompt_toolkit import prompt
from json import dumps

# global variables
DBPATH = './database/accounts.json'
IDLENGTH = 32

def generate_account_id(length: int) -> str:
    characters = digits + ascii_letters
    accountId = ""
    for _ in range(length):
        accountId += choice(characters)
    return accountId


def generate_password(length: int) -> str:
    characters = digits + ascii_letters + punctuation 
    password = ""
    for _ in range(length):
        password += choice(characters)
    return password


def password_check() -> str:
    while True:
        passNew = getpass("Enter the new password: ")
        passCon = getpass("Confrim the new password: ")
        if passNew == passCon:
            return passNew
        print("Passwords do not match. Try again")


def load_db(dbpath: str, masterPass: str) -> dict:
    dbData = data_base.read(dbpath)

    if len(dbData['accounts']) == 0:
        print(f"No accounts found in the database '{dbpath}'")
        return None

    decryptedData = {}
    try: 
        for ID in dbData['accounts']:
            decryptedAccount = crypt.decrypt(dbData['accounts'][ID], masterPass)
            decryptedData[ID] = decryptedAccount
    except Exception as e:
        print(f"Failed to decrypt accounts: {e}")
        exit()

    return decryptedData


def edit_account(dbpath: str, accountId: str, masterPass: str) -> None:
    dbData = data_base.read(dbpath)

    if accountId not in dbData['accounts']:
        print(f"Account with ID '{accountId}' not found in the database.")
        return
    
    encryptedAccount = dbData['accounts'][accountId]
    decryptedAccount = crypt.decrypt(encryptedAccount, masterPass)

    editedAccount = {
        'name': prompt("Edit The account Name: ", default=decryptedAccount['name']),
        'label': prompt("Edit The account Labels: ", default=decryptedAccount['label']),
        'password': password_check
    }

    encryptAccount = crypt.encrypt(dumps(editedAccount), masterPass)
    dbData['accounts'][accountId] = encryptAccount
    data_base.write(dbpath, dbData)


def add_account(dbpath: str, masterPass: str) -> None:
    newAccountId = generate_account_id(IDLENGTH)
    newAccount = {
        'name': input("Enter the new account name: "),
        'label': input("Enter a label name: "),
        'password': password_check
    }
    encryptedAccount = crypt.encrypt(dumps(newAccount), masterPass)

    dbData = data_base.read(dbpath)
    dbData['accounts'][newAccountId] = encryptedAccount
    data_base.write(dbpath, dbData)


masterPass = getpass(F"Enter the master password for '{DBPATH}': ")
accounts = load_db(DBPATH, masterPass)
print(accounts)
