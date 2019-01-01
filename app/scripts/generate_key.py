from base64 import b64encode

from Crypto.PublicKey import RSA

SECRET_KEY_PATH = './secret_key3.txt'
PUBLIC_KEY_PATH = './public_key3.txt'


def generate_key(keysize = 2048, passphrase = None):
    new_key = RSA.generate(keysize)
    public_key = new_key.publickey().exportKey()
    secret_key = new_key.exportKey(passphrase = passphrase)
    return secret_key, public_key


if __name__ == "__main__":
    secret_key, public_key = generate_key()

    with open(SECRET_KEY_PATH, mode = 'w') as f:
        f.write(str(secret_key.decode('utf-8')))

    with open(PUBLIC_KEY_PATH, mode = 'w') as f:
        f.write(str(public_key.decode('utf-8')))
