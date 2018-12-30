import json
import sys
from base64 import b64decode

import requests

from app.scripts.get_public_key import get_public_key
from app.scripts.get_secret_key import get_secret_key
from app.scripts.sign import sign

URL = 'http://localhost:5001/transactions'


if __name__ == '__main__':
    amount = int(sys.argv[1])
    recipient_address = sys.argv[2]
    sender_address = get_public_key()

    secret_key = get_secret_key()

    unlocking_script = sign(secret_key, '1')

    payload = {
        'sender_address': sender_address,
        'recipient_address': recipient_address,
        'amount': amount,
        'transaction_inputs': [
            {
                'transaction_output_id': 1,
                'unlocking_script': unlocking_script
            }
        ]
    }

    headers = { 'content-type': 'application/json' }
    res = requests.post(URL, data = json.dumps(payload), headers = headers)
    print(res)