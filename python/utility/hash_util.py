"""Import hashlib and json."""
import hashlib
import json


def hash_string_256(string):
    """Return a 64 character hex string.

    Arguments:
    ---------
        string : str
            String to be hashed.

    """
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Output a hash for a given input block.

    Arguments:
    ---------
        block : str
            Block that to be hashed.

    """
    hashable_block = block.__dict__.copy()
    hashable_block["transactions"] = [
        tx.to_ordered_dict() for tx in hashable_block["transactions"]
    ]
    return hash_string_256(
        json.dumps(hashable_block, sort_keys=True).encode()
    )
