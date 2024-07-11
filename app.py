import json
import os

from scripts import decryption, encryption

dataBasePath = 'database/accounts.json'

masterpassword = "1"

def read(database):
    with open(database, "r") as file:
        data = json.load(file)
    return data

def encrypt(account):
    data = read(dataBasePath)
    encrypted = encryption.main(account[1], masterpassword)
    newpassword = {
        'label': account[2],
        'password': encrypted,
    }
    data['accounts'][account[0]] = newpassword
    print(data)
    with open(dataBasePath, "w") as outfile:
        json.dump(data, outfile)

def decrypt(database):
    data = read(dataBasePath)
    try:
        for account in data['accounts']:
            decrypted = decryption.main(data['accounts'][account]["password"], masterpassword)
            print(account, decrypted)
    except:
        print("incorrect password: gfys")
    
decrypt(dataBasePath)
# encrypt(account1)
# encrypt(account2)
# encrypt(account3)


# # # Let us decrypt using our original password
# # decrypted = decryption.main(data, password)
# # print(bytes.decode(decrypted))
