from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)


@app.route("/", methods=["GET"])
def get_ui():
    return send_from_directory("ui", "node.html")


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {"message": "Saving the keys failed."}
        return jsonify(response), 500


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {"message": "Loading the keys failed."}
        return jsonify(response), 500


@app.route("/balance", methods=["GET"])
def get_balance():
    balance = blockchain.get_balance()
    if balance is not None:
        response = {
            "message": "Fetched balance successfully.",
            "funds": balance,
        }
        return jsonify(response), 200
    else:
        response = {
            "message": "Loading response failed.",
            "wallet_set_up": wallet.public_key is not None,
        }
        return jsonify(response), 500


@app.route("/transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key is None:
        response = {"message": "No wallet found."}
        return jsonify(response), 400
    values = request.get_json()
    if not values:
        response = {"message": "No data found."}
        return jsonify(response), 400
    required_fields = ["receiver", "amount"]
    if not all(field in values for field in required_fields):
        response = {"message": "Required data is missing."}
        return jsonify(response), 400
    receiver = values["receiver"]
    amount = values["amount"]
    signature = wallet.sign_transaction(wallet.public_key, receiver, amount)
    success = blockchain.add_transaction(
        receiver, wallet.public_key, signature, amount
    )
    if success:
        response = {
            "message": "Successfully added transaction.",
            "transaction": {
                "sender": wallet.public_key,
                "receiver": receiver,
                "amount": amount,
                "signature": signature,
            },
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {"message": "Creating a transaction failed."}
        return jsonify(response), 500


@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine_block()
    if block is not None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [
            tx.__dict__ for tx in dict_block["transactions"]
        ]
        response = {
            "message": "Block successfully mined.",
            "block": dict_block,
            "funds": blockchain.get_balance(),
        }
        return jsonify(response), 201
    else:
        response = {
            "message": "Mining a block failed.",
            "wallet_set_up": wallet.public_key is not None,
        }
        return jsonify(response), 500


@app.route("/transactions", methods=["GET"])
def open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@app.route("/chain", methods=["GET"])
def get_chain():
    chain = blockchain.chain
    dict_chain = [
        [tx.__dict__ for tx in block.__dict__.copy()["transactions"]]
        for block in chain
    ]
    return jsonify(dict_chain), 200


if __name__ == "__main__":
    app.run()
