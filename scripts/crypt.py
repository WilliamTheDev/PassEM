import hashlib
import json 

from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes as getRandomBytes

# encrypts 
def encrypt(account: str, masterPass: str) -> list:
    # generate a random salt
    salt = getRandomBytes(AES.block_size)

    # use the Scrypt KDF to get a private key from the password
    privateKey = hashlib.scrypt(masterPass.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    # create cipher config
    cipherConfig = AES.new(privateKey, AES.MODE_GCM)

    # return a dictionary with the encrypted text
    encryptedText, tag = cipherConfig.encrypt_and_digest(bytes(account, 'utf-8'))
    return {
        'account': b64encode(encryptedText).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipherConfig.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

# Decrypts 
def decrypt(encryptedAccount: list, password: str) -> dict:
    # decode the dictionary entries from base64
    account = b64decode(encryptedAccount['account'])
    salt = b64decode(encryptedAccount['salt'])
    nonce = b64decode(encryptedAccount['nonce'])
    tag = b64decode(encryptedAccount['tag'])

    # generate the private key & cipher config
    privateKey = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    cipherConfig = AES.new(privateKey, AES.MODE_GCM, nonce=nonce)

    # decrypts the account 
    decryptedAccount = cipherConfig.decrypt_and_verify(account, tag)
    decodeAccount = decryptedAccount.decode('utf-8') 
    jsonAccount = json.loads(decodeAccount.replace("'", '"'))  

    return jsonAccount 


