PUBLIC_KEY_PATH = './public_key.txt'


def get_public_key():
    with open(PUBLIC_KEY_PATH) as f:
        s = f.read()
        return s
