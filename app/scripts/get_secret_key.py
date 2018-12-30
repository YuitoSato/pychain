def get_secret_key():
    with open('./secret_key.txt') as f:
        s = f.read()
        return s
