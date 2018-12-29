class Transaction:
    def __init__(
        self,
        transaction_id,
        transaction_outputs,
        transaction_inputs,
        locktime
    ):
        self.transaction_id = transaction_id
        self.transaction_outputs = transaction_outputs
        self.transaction_inputs = transaction_inputs
        self.locktime = locktime
