from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode, b64encode
import sys

def generate_key(keysize=2048, passphrase = None):
    new_key = RSA.generate(keysize)
    public_key = new_key.publickey().exportKey()
    secret_key = new_key.exportKey(passphrase = passphrase)
    return secret_key, public_key

def sign(secret_key, data, passphrase = None):
    try:
        rsakey = RSA.importKey(secret_key, passphrase = passphrase)
    except ValueError as e:
        print(e)
        sys.exit(1)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    sign = signer.sign(digest)
    return b64encode(sign)

def verify(pub_key, signature, data):
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(b64decode(data))
    if signer.verify(digest, b64decode(signature)):
        return True
    else:
        return False


# 秘密鍵と公開鍵を作る。（パスワードはなくても良い）
password = "password"
sk, pk = generate_key(passphrase = password)
print(sk)
print(pk)

# メッセージに署名する（署名者が行う）
message = "hoge"
sig = sign(sk, message, passphrase = password)

#　承認テスト（承認者が行う）
if verify(pk, sig, message):
    print("承認 OK")
else:
    print("承認 NG")

#　メッセージの書き換えに対するテスト
changed_message = "hogehoge"
if verify(pk, sig, changed_message):
    print("書き換えテスト NG")
else:
    print("書き換えテスト OK") # 承認されなければOK

# 間違った秘密鍵の署名に対するテスト
sk2, pk2 = generate_key(passphrase = password)
sig2 = sign(sk2, message, passphrase = password)
if verify(pk, sig2, message):
    print("不正署名テスト NG")
else:
    print("不正署名テスト OK") # 承認されなければOK