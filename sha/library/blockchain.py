from .block import Block


# --- This class is used for blockchain and it stores blocks
class Blockchain:
    # --- This function can defines chain
    def __init__(self):
        self.chain = []

    # --- This function create genesis blocks
    @staticmethod
    def create_genesis_block():
        return Block(0, "01/01/2021", "Genesis block", "0")

    # --- This function get last block
    def get_last_block(self):
        if len(self.chain) > 0:
            return self.chain[-1]
        else:
            # --- Handle the case when the chain is empty
            # print("The chain is empty. Genesis block created!")
            genesis_block = self.create_genesis_block()
            self.chain.append(genesis_block)
            return genesis_block

    # --- This function add blocks to the blockchain
    def add_block(self, new_block, address):
        # --- Get the previous block
        previous_block = self.get_last_block()
        if previous_block is not None:
            new_block.previous_hash = previous_block.hash
        else:
            new_block.previous_hash = ""
        new_block.hash = new_block.generate_hash(address)
        self.chain.append(new_block)

    def has_block(self, block):
        return block in self.chain
