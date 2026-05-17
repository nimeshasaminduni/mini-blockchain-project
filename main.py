import hashlib
import datetime
import json
import random


# =========================
# BLOCK CLASS
# =========================

class Block:

    def __init__(self, index, transactions, previous_hash):

        self.index = index

        self.timestamp = str(datetime.datetime.now())

        self.transactions = transactions

        self.previous_hash = previous_hash

        self.nonce = 0

        self.merkle_root = self.calculate_merkle_root()

        self.hash = self.calculate_hash()

    # -------------------------
    # Calculate Merkle Root
    # -------------------------

    def calculate_merkle_root(self):

        transaction_hashes = []

        for tx in self.transactions:

            tx_hash = hashlib.sha256(
                json.dumps(tx).encode()
            ).hexdigest()

            transaction_hashes.append(tx_hash)

        if len(transaction_hashes) == 0:
            return ""

        while len(transaction_hashes) > 1:

            temp_list = []

            for i in range(0, len(transaction_hashes), 2):

                left = transaction_hashes[i]

                if i + 1 < len(transaction_hashes):
                    right = transaction_hashes[i + 1]
                else:
                    right = left

                combined = left + right

                combined_hash = hashlib.sha256(
                    combined.encode()
                ).hexdigest()

                temp_list.append(combined_hash)

            transaction_hashes = temp_list

        return transaction_hashes[0]

    # -------------------------
    # Calculate Block Hash
    # -------------------------

    def calculate_hash(self):

        block_string = (
            str(self.index) +
            self.timestamp +
            json.dumps(self.transactions) +
            self.previous_hash +
            str(self.nonce) +
            self.merkle_root
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()

    # -------------------------
    # Mining Function
    # -------------------------

    def mine_block(self, difficulty):

        target = "0" * difficulty

        print(f"\nMining Block {self.index}...")

        while self.hash[:difficulty] != target:

            self.nonce += 1

            self.hash = self.calculate_hash()

        print("Block Mined!")
        print("Hash:", self.hash)


# =========================
# BLOCKCHAIN CLASS
# =========================

class Blockchain:

    def __init__(self):

        self.chain = [self.create_genesis_block()]

        self.difficulty = 4

        self.pending_transactions = []

    # -------------------------
    # Genesis Block
    # -------------------------

    def create_genesis_block(self):

        return Block(
            0,
            [{"message": "Genesis Block"}],
            "0"
        )

    # -------------------------
    # Get Latest Block
    # -------------------------

    def get_latest_block(self):

        return self.chain[-1]

    # -------------------------
    # Add Transaction
    # -------------------------

    def add_transaction(
            self,
            sender,
            receiver,
            amount
    ):

        transaction = {
            "from": sender,
            "to": receiver,
            "amount": amount
        }

        self.pending_transactions.append(transaction)

    # -------------------------
    # Mine Pending Transactions
    # -------------------------

    def mine_pending_transactions(self):

        block = Block(
            len(self.chain),
            self.pending_transactions,
            self.get_latest_block().hash
        )

        block.mine_block(self.difficulty)

        self.chain.append(block)

        self.pending_transactions = []

        # Difficulty increase
        if len(self.chain) % 2 == 0:

            self.difficulty += 1

            print(
                "\nDifficulty Increased To:",
                self.difficulty
            )

    # -------------------------
    # Validate Blockchain
    # -------------------------

    def is_chain_valid(self):

        for i in range(1, len(self.chain)):

            current_block = self.chain[i]

            previous_block = self.chain[i - 1]

            # Recalculate hash
            if current_block.hash != current_block.calculate_hash():

                print("Invalid Hash at Block", i)

                return False

            # Check previous hash
            if current_block.previous_hash != previous_block.hash:

                print("Broken Chain at Block", i)

                return False

        return True

    # -------------------------
    # Display Blockchain
    # -------------------------

    def display_chain(self):

        for block in self.chain:

            print("\n=========================")

            print("Block Index:", block.index)

            print("Timestamp:", block.timestamp)

            print("Transactions:")

            for tx in block.transactions:
                print(tx)

            print("Merkle Root:", block.merkle_root)

            print("Nonce:", block.nonce)

            print("Previous Hash:", block.previous_hash)

            print("Hash:", block.hash)

            print("=========================")


# =========================
# SIMPLE PROOF OF STAKE
# =========================

def proof_of_stake_demo():

    print("\n===== Proof of Stake Demo =====")

    validators = {
        "Alice": 100,
        "Bob": 50,
        "Charlie": 200
    }

    selected = random.choices(
        list(validators.keys()),
        weights=validators.values()
    )

    print("Selected Validator:", selected[0])


# =========================
# MAIN PROGRAM
# =========================

my_blockchain = Blockchain()

# -------------------------
# Add Transactions
# -------------------------

my_blockchain.add_transaction(
    "wallet_A",
    "wallet_B",
    5
)

my_blockchain.add_transaction(
    "wallet_C",
    "wallet_D",
    2
)

# -------------------------
# Mine Block 1
# -------------------------

my_blockchain.mine_pending_transactions()

# -------------------------
# Add More Transactions
# -------------------------

my_blockchain.add_transaction(
    "wallet_E",
    "wallet_F",
    10
)

my_blockchain.add_transaction(
    "wallet_G",
    "wallet_H",
    7
)

# -------------------------
# Mine Block 2
# -------------------------

my_blockchain.mine_pending_transactions()

# -------------------------
# Display Blockchain
# -------------------------

my_blockchain.display_chain()

# -------------------------
# Validate Blockchain
# -------------------------

print("\nIs Blockchain Valid?")

print(my_blockchain.is_chain_valid())

# -------------------------
# Proof of Stake Demo
# -------------------------

proof_of_stake_demo()
