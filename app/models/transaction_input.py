class TransactionInput:
    def __init__(self, transaction_input_id, transaction_id, transaction_output_id, unlocking_script):
        self.transaction_input_id = transaction_input_id
        self.transaction_id = transaction_id
        self.transaction_output_id = transaction_output_id
        self.unlocking_script = unlocking_script
