"""Import OrderedDict module."""
from collections import OrderedDict


class Transaction:
    """A blockchain transaction."""

    def __init__(self, sender, receiver, signature, amount):
        """Initialize Transaction."""
        self.sender = sender
        self.receiver = receiver
        self.signature = signature
        self.amount = amount

    def __repr__(self):
        """Return default transaction string."""
        return str(
            "\nSender: {}\nReceiver: {:}\nAmount: {:} coins\n".format(
                self.sender, self.receiver, self.amount
            )
        )

    def to_ordered_dict(self):
        """Return transaction as an ordered dictionary."""
        return OrderedDict(
            [
                ("sender", self.sender),
                ("receiver", self.receiver),
                ("amount", self.amount),
            ]
        )
