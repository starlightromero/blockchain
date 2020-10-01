"""Import  modules."""
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet


class Node:
    """The Node."""

    def __init__(self):
        """Initialize Node."""
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def get_transaction_data(self):
        """Get user input for a new transaction."""
        print("{:-^80}".format("NEW TRANSACTION"))
        tx_receiver = input("Enter the receiver: ")
        tx_amount = float(input("Enter the amount: "))
        return tx_receiver, tx_amount

    def print_blocks_in_blockchain(self):
        """Output the blockchain list to the console."""
        for block in self.blockchain.chain:
            print("{:-^80}".format("OUTPUTTING BLOCK"))
            print(block)
        else:
            print("{:-^80}\n".format(""))

    def boot_blockchain(self):
        """Introduction to the blockchain."""
        print("{:-^80}\n".format("Welcome to the blockchain").upper())
        if self.wallet.public_key is None:
            print(
                "{:-^80}\n".format(
                    "No wallet detected. Please create wallet."
                ).upper()
            )

    def add_new_transaction(self):
        """Allow the user to add  a new transaction to the blockchian."""
        tx_data = self.get_transaction_data()
        receiver, amount = tx_data
        signature = self.wallet.sign_transaction(
            self.wallet.public_key, receiver, amount
        )
        if self.blockchain.add_transaction(
            receiver, self.wallet.public_key, signature, amount=amount
        ):
            print("{:-^80}\n".format("Transaction successful").upper())
        else:
            print(
                "{:-^80}\n".format(
                    "Transaction failed(Insufficient funds)"
                ).upper()
            )

    def mine_new_block(self):
        """Allow the user to mine a new block."""
        print("{:-^80}\n".format("Mining in progress").upper())
        if not self.blockchain.mine_block():
            print("{:-^80}".format("Mining failed(No wallet found)").upper())

    def verify_all_transactions(self):
        """Allow the user to verify all blockchain transactions."""
        if Verification.verify_transactions(
            self.blockchain.get_open_transactions(),
            self.blockchain.get_balance,
        ):
            print("{:-^80}\n".format("All transactions are valid").upper())
        else:
            print(
                "{:-^80}\n".format("There are invalid transactions.").upper()
            )

    def create_wallet(self):
        """Create a new wallet for the user."""
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def load_wallet(self):
        """Load a wallet for the user."""
        self.wallet.load_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def check_invalid_blockchain(self):
        """Check the validity of the blockchain."""
        if not Verification.verify_chain(self.blockchain.chain):
            self.print_blocks_in_blockchain()
            print("{:-^80}\n".format("INVALID BLOCKCHAIN!") * 10)

    def user_balance(self):
        """Display the user's balance."""
        balance = "{} {:1.2f} {}".format(
            "{} balance is".format(self.wallet.public_key),
            self.blockchain.get_balance(),
            "coins",
        ).upper()
        print("{:-^80}\n".format(balance))

    def exit_blockchain(self):
        """End blockchain message."""
        print("{:-^80}".format("Thank you for using the blockchain").upper())

    def get_user_input(self):
        """Get user input."""
        print("{:-^80}".format("Waiting for input").upper())
        print("1: Add a new transaction")
        print("2: Mine a new block")
        print("3: Output the blockchain blocks")
        print("4: Verify all transactions")
        print("5: Create wallet")
        print("6: Load wallet")
        print("7: Save keys")
        print("q: Quit")
        return input("Your input: ".upper())

    def listen_for_input(self):
        """Blockchain user interface."""
        self.boot_blockchain()
        waiting_for_input = True
        while waiting_for_input:
            user_choice = self.get_user_input()
            if user_choice == "1":
                self.add_new_transaction()
            elif user_choice == "2":
                self.mine_new_block()
            elif user_choice == "3":
                self.print_blocks_in_blockchain()
            elif user_choice == "4":
                self.verify_all_transactions()
            elif user_choice == "5":
                self.create_wallet()
            elif user_choice == "6":
                self.load_wallet()
            elif user_choice == "7":
                self.wallet.save_keys()
            elif user_choice == "q":
                waiting_for_input = False
            else:
                print("{:-^80}\n".format("INVALID INPUT!"))
            if self.check_invalid_blockchain() is False:
                break
            self.user_balance()
        else:
            self.exit_blockchain()


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
