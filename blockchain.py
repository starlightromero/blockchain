"""Import modules and set mining reward."""
from functools import reduce
import json
import requests
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet


MINING_REWARD = 10


class Blockchain:
    """The Blockchain class manages the chain of blocks as well as open transactions and the node on which it's running.

    Attributes:
    ---------
        chain : list
            The list of blocks
        open_transactions (private) : list
            The list of open transactions
        public_key : str
            The connected node (which runs the blockchain).

    """

    def __init__(self, public_key, node_id):
        """Initialize and load blockchain."""
        genesis_block = Block(0, "", [], 100, 0)
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.load_data()

    @property
    def chain(self):
        """Chain getter."""
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        """Chain setter."""
        self.__chain = val

    def get_open_transactions(self):
        """Open transactions getter."""
        return self.__open_transactions[:]

    def load_data(self):
        """Load blockchain from txt file."""
        try:
            with open(f"blockchain-{self.node_id}.txt", mode="r") as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [
                        Transaction(
                            tx["sender"],
                            tx["receiver"],
                            tx["signature"],
                            tx["amount"],
                        )
                        for tx in block["transactions"]
                    ]
                    updated_block = Block(
                        block["index"],
                        block["previous_hash"],
                        converted_tx,
                        block["proof"],
                        block["timestamp"],
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx["sender"],
                        tx["receiver"],
                        tx["signature"],
                        tx["amount"],
                    )
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.load(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            pass

    def save_data(self):
        """Save blockchain to txt file."""
        try:
            with open(f"blockchain-{self.node_id}.txt", mode="w") as f:
                saveable_chain = [
                    block.__dict__
                    for block in [
                        Block(
                            block_el.index,
                            block_el.previous_hash,
                            [tx.__dict__ for tx in block_el.transactions],
                            block_el.proof,
                            block_el.timestamp,
                        )
                        for block_el in self.__chain
                    ]
                ]
                f.write(json.dumps(saveable_chain))
                f.write("\n")
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                f.write(json.dumps(list(self.__peer_nodes)))
        except IOError:
            print("{:-^80}".format("Saving failed").upper())

    def proof_of_work(self):
        """Generate proof of work for open transactions."""
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(
            self.__open_transactions, last_hash, proof
        ):
            proof += 1
        return proof

    def get_balance(self, sender=None):
        """Return current balance of the sender node."""
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [
            [
                tx.amount
                for tx in block.transactions
                if tx.sender == participant
            ]
            for block in self.__chain
        ]
        open_tx_sender = [
            tx.amount
            for tx in self.__open_transactions
            if tx.sender == participant
        ]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0
            else tx_sum + 0,
            tx_sender,
            0,
        )

        tx_receiver = [
            [
                tx.amount
                for tx in block.transactions
                if tx.receiver == participant
            ]
            for block in self.__chain
        ]
        amount_received = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0
            else tx_sum + 0,
            tx_receiver,
            0,
        )

        return amount_received - amount_sent

    def get_last_block(self):
        """Return the last block of the current blockchain."""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(
        self, receiver, sender, signature, amount=1.0, is_receiving=False
    ):
        """Append a new transaction to the list of open transactions.

        Arguments:
        ---------
            receiver : str
                The recipient of the coins.
            sender : str
                The sender of the coins.
            amount : str
                The amount of coins sent with the transaction (default = 1.0)
            signature : str
                Signature

        """
        if self.public_key is None:
            return False
        transaction = Transaction(sender, receiver, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = f"http://{node}/broadcast-transaction"
                    try:
                        response = requests.post(
                            url,
                            json={
                                "sender": sender,
                                "receiver": receiver,
                                "signature": signature,
                            },
                        )
                        if (
                            response.status_code == 400
                            or response.status_code == 500
                        ):
                            print("Transaction declined. Needs resolving.")
                            return False
                    except requests.exceptions.ConnectionError:
                        continue
            return True
        return False

    def mine_block(self):
        """Append list of open transactions to the blockchain."""
        if self.public_key is None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        reward_transaction = Transaction(
            "MINING", self.public_key, "", MINING_REWARD
        )
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(
            len(self.__chain), hashed_block, copied_transactions, proof
        )
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = f"http://{node}/broadcast_block"
            converted_block = block.__dict__.copy()
            converted_block["transactions"] = [
                tx.__dict__ for tx in converted_block["transactions"]
            ]
            try:
                response = requests.post(url, json={"block": converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined. Needs resolving.")
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        transactions = [
            Transaction(
                tx["sender"], tx["receiver"], tx["signature"], tx["amount"]
            )
            for tx in block["transactions"]
        ]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block["previous_hash"], block["proof"]
        )
        hashes_match = hash(self.chain[-1]) == block["previous_hash"]
        if not proof_is_valid or not hashes_match:
            return False
        converted_block = Block(
            block["index"],
            block["previous_hash"],
            transactions,
            block["proof"],
            block["timestamp"],
        )
        self.__chain.append(converted_block)
        self.save_data()
        return True

    def add_peer_node(self, node):
        """Add a new node to the peer node set.

        Arguments:
        ---------
            node : str
                The node URL which should be added.

        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Remove a node from the peer node set.

        Arguments:
        ---------
            node : str
                The node URL which should be removed.

        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes."""
        return list(self.__peer_nodes)
