
# --- This class is for validators. In this class we can create validators, join validators to each other
# --- validate block with checking stake of each validators
class Validator:
    # --- This function define attribute of validators
    def __init__(self, env, name, stake, blockchain, address):
        self.env = env
        self.name = name
        self.blockchain = blockchain
        self.peers = []
        self.stake = stake
        self.address = address
        self.last_block_received = None
        self.num_transactions_processed = 0
        self.energy_consumed = 0

    # --- This function add peers to each other
    def add_peer(self, peer):
        self.peers.append(peer)

    # --- This function send blocks for validation
    def receive_block(self, block):
        if self.validate_block(block) and not self.blockchain.has_block(block):
            self.last_block_received = block
            address = self.address
            self.blockchain.add_block(block, address)
            self.num_transactions_processed += 1    # --- Number of transaction(or Block) processed by this validator
            self.energy_consumed += 1               # --- Simulate consumed by this validator to validate the block
            for peer in self.peers:
                peer.receive_block(block)

    # --- This function validate block by validators
    def validate_block(self, block):
        if block.index == 0:
            return True     # --- Genesis block always valid
        if block.previous_hash == self.blockchain.get_last_block().hash:
            return False    # --- Invalid previous hash
        if not self.check_stake(block):
            return False    # --- Invalid proof-of-stake data
        return True

    # --- This function defines which validator can be selected as forger
    def check_stake(self, block):
        # --- Verify the proof-of-stake data in the block based on the validator's stake and age of coins
        max_age = 1                                     # --- Maximum age of coins allowed for staking (e.g. 1 second)
        maturity = int(self.env.now - block.timestamp)  # --- Age of the coins being staked
        time_factor = 1 - min(maturity / max_age, 1)    # --- Stake age factor in range [0, 1]

        # --- Check if denominator is zero
        if sum(validator.stake for validator in self.peers) == 0:
            return False

        # --- Verify the proof-of-stake data based on the validator's stake
        block_hash = block.hash
        threshold = (self.stake / sum(validator.stake for validator in self.peers)) * time_factor
        return int(block_hash, 16) / int("f" * 64, 16) <= threshold
