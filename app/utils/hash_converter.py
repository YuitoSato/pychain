import hashlib
import json

from app.utils.pychain_encoder import PychainEncoder


class HashConverter:
    def __init__(self, encoder):
        self.encoder = encoder

    def hash(self, obj):
        object_string = json.dumps(obj, sort_keys=True, cls=self.encoder).encode()
        return hashlib.sha256(object_string).hexdigest()
