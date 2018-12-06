from app.models.block import Block


def decode_block(request):
    values = request.get_json()
    return Block(
        index = values['index'],
        transactions = values['transactions'],
        timestamp = values['timestamp'],
        nonce = values['nonce'],
        previous_hash = values['previous_hash'],
        difficulty = values['difficulty']
    )
