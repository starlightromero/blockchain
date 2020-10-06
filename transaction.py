"""Import OrderedDict module."""
from collections import OrderedDict


class Transaction:
    """A blockchain transaction.

    Arguements
    ---------
        sender
            The sender of the coins.
        receiver
            The receiver of the coins.
        signature
            The signature of the transaction.
        amount
            The amount of coins sent.

    """

    def __init__(self, sender, receiver, signature, amount):
        """Initialize Transaction."""
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.amount = amount

    def __repr__(self):
        return str(self.__dict__)

    def to_ordered_dict(self):
        """Return transaction as an ordered dictionary."""
        return OrderedDict(
            [
                ("sender", self.sender),
                ("receiver", self.receiver),
                ("amount", self.amount),
            ]
        )
