import sys
from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256


def get_public_key():
    with open('./public_key.txt') as f:
        s = f.read()
        return RSA.importKey(s.encode('utf-8'))


if __name__ == '__main__':
    data = sys.argv[1]
    public_key = get_public_key()
    encryptor = PKCS1_OAEP.new(public_key, SHA256)
    encrypted = encryptor.encrypt(data.encode('utf-8'))
    print(encrypted.decode('latin-1'))
    # print(encrypted.decode("utf-8"))
    # print(b64decode(encrypted))
    # print(b64decode(encrypted + bytes('/' * (-len(encrypted) % 4))))
