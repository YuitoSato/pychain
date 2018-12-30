import base64

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys

from app.scripts.lock import get_public_key

SECRET_KEY_PATH = './secret_key.txt'

get_public_key()


def sign(secret_key, data, passphrase = None):
    try:
        rsakey = RSA.importKey(secret_key, passphrase = passphrase)
    except ValueError as e:
        print(e)
        sys.exit(1)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    encoded = (data + ('/' * (-len(data) % 4))).encode('utf-8')
    b64decoded = b64decode(encoded)
    digest.update(b64decoded)

    sign = signer.sign(digest)
    return b64encode(sign).decode('utf-8')


def get_secret_key():
    with open(SECRET_KEY_PATH) as f:
        s = f.read()
        return s.encode('utf-8')


if __name__ == '__main__':
    data = sys.argv[1]
    secret_key = get_secret_key()
    print(sign(secret_key, data))
