from app.models.block import Block
from app.models.transaction import Transaction
from app.models.transaction_input import TransactionInput
from app.models.transaction_output import TransactionOutput
from app.models.proof_result import ProofResult


def decode_blocks(dicts):
    return list(map(lambda dictionary: decode_block(dictionary), dicts))


def decode_block(dictionary):
    if dictionary['transactions'] is not None:
        transactions = decode_transactions(dictionary['transactions'])
    else:
        transactions = None

    return Block(
        block_id = dictionary['block_id'],
        block_number = dictionary['block_number'],
        version = dictionary['version'],
        previous_block_hash = dictionary['previous_block_hash'],
        timestamp = dictionary['timestamp'],
        merkle_root = dictionary['merkle_root'],
        difficulty_target = dictionary['difficulty_target'],
        nonce = dictionary['nonce'],
        transactions = transactions
    )


def decode_transactions(dicts):
    return list(map(lambda dictionary: decode_transaction(dictionary), dicts))


def decode_transaction(dictionary):
    if dictionary['transaction_outputs'] is not None:
        transaction_outputs = decode_transaction_outputs(dictionary['transaction_outputs'])
    else:
        transaction_outputs = None

    if dictionary['transaction_inputs'] is not None:
        transaction_inputs = decode_transaction_inputs(dictionary['transaction_inputs'])
    else:
        transaction_inputs = None

    return Transaction(
        transaction_id = dictionary['transaction_id'],
        block_id = dictionary['block_id'],
        locktime = dictionary['locktime'],
        transaction_inputs = transaction_inputs,
        transaction_outputs = transaction_outputs
    )


def decode_transaction_outputs(dicts):
    return list(map(lambda dictionary: decode_transaction_output(dictionary), dicts))


def decode_transaction_output(dictionary):
    return TransactionOutput(
        transaction_output_id = dictionary['transaction_output_id'],
        transaction_id = dictionary['transaction_id'],
        amount = dictionary['amount'],
        locking_script = dictionary['locking_script'],
        sender_address = dictionary['sender_address'],
        recipient_address = dictionary['recipient_address']
    )


def decode_transaction_inputs(dicts):
    return list(map(lambda dictionary: decode_transaction_input(dictionary), dicts))


def decode_transaction_input(dictionary):
    return TransactionInput(
        transaction_input_id = dictionary['transaction_input_id'],
        transaction_id = dictionary['transaction_id'],
        transaction_output_id = dictionary['transaction_output_id'],
        unlocking_script = dictionary['unlocking_script']
    )


def decode_proof_result(dictionary):
    return ProofResult(
        result_hash_int = dictionary['result_hash_int'],
        target_hash_int = dictionary['target_hash_int'],
        nonce = dictionary['nonce']
    )
