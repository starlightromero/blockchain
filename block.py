"""Import time library."""
from time import time


class Block:
    """A Block of Blockchain."""

    def __init__(
        self, index, previous_hash, transactions, proof, timestamp=time()
    ):
        """Initialize Block."""
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.proof = proof
        self.timestamp = timestamp

    def __repr__(self):
        """Return a dict of Block."""
        return str(self.__dict__)
