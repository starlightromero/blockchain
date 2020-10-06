"""Import modules for keys."""
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    """Access keys for Wallet of blockchain user."""

    def __init__(self, node_id):
        """Initialize Wallet."""
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        """Create a new private and public key pair."""
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        """Save private and public keys to a file."""
        if self.private_key is not None and self.public_key is not None:
            try:
                with open(f"wallet-{self.node_id}.txt", mode="w") as f:
                    f.write(self.public_key)
                    f.write("\n")
                    f.write(self.private_key)
                    return True
            except (IOError, IndexError):
                print("{:-^80}".format("Saving wallet failed.").upper())
                return False

    def load_keys(self):
        """Load private and public keys from a file."""
        try:
            with open(f"wallet-{self.node_id}.txt", mode="r") as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print("{:-^80}".format("Loading wallet failed.").upper())
            return False

    def generate_keys(self):
        """Generate new private and public keys."""
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (
            binascii.hexlify(private_key.exportKey(format="DER")).decode(
                "ascii"
            ),
            binascii.hexlify(public_key.exportKey(format="DER")).decode(
                "ascii"
            ),
        )

    def sign_transaction(self, sender, receiver, amount):
        """Return a signature for a given transaction.

        Arguments:
        ---------
            sender : str
                The sender of the transaction.
            receiver : str
                The receiver of the transaction.
            amount : str
                The amount of the transaction.

        """
        signer = PKCS1_v1_5.new(
            RSA.importKey(binascii.unhexlify(self.private_key))
        )
        h = SHA256.new(
            (str(sender) + str(receiver) + str(amount)).encode("utf8")
        )
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode("ascii")

    @staticmethod
    def verify_transaction(transaction):
        """Verify signature of a transaction.

        Arguments:
        ---------
            transaction : str
                The transaction to be verified.

        """
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new(
            (
                str(transaction.sender)
                + str(transaction.receiver)
                + str(transaction.amount)
            ).encode("utf8")
        )
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
