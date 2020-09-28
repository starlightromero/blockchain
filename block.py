"""Import time library."""
from time import time


class Block:
    """A Block of Blockchain."""

    def __init__(
        self, index, previous_hash, transactions, proof, timestamp=None
    ):
        """Initialize Block."""
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = time() if timestamp is None else timestamp

    def __repr__(self):
        """Return the default."""
        return (
            "Index: {}, Previous Hash: {}, Transactions: {}, Proof {}".format(
                self.index, self.previous_hash, self.transactions, self.proof
            )
        )
