from blake3 import blake3


# --- This class is used to create Block and also create the hash of the Block with BLAKE3
class Block:
    # --- This function is defining attribute of Block
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.generate_hash()
        self.nonce = nonce

    # --- This function create hash of the Block
    def generate_hash(self, address="Node Address"):
        data_str = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(address)
        hash_object = blake3(data_str.encode())
        return hash_object.hexdigest()
