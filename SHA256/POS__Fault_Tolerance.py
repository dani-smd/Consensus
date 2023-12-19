import simpy
from sha256 import sha256
import random
import time
# ---
from ProofOfStake import ProofOfStake
from os.path import exists
import jsonpickle
import string
import json
import os


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
        hash_object = sha256(data_str.encode())
        return hash_object.hexdigest()


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

        # --- Initialize faulty flag to False
        self.faulty = False

    # --- This function add peers to each other
    def add_peer(self, peer):
        self.peers.append(peer)

    # --- This function send blocks for validation
    def receive_block(self, block):
        if self.validate_block(block) and not self.blockchain.has_block(block):
            self.last_block_received = block
            address = self.address
            self.blockchain.add_block(block, address)
            for peer in self.peers:
                peer.receive_block(block)

    # --- This function validate block by validators
    def validate_block(self, block):
        if block.index == 0:
            return True  # --- Genesis block always valid
        if block.previous_hash == self.blockchain.get_last_block().hash:
            return False  # --- Invalid previous hash
        if not self.check_stake(block):
            return False  # --- Invalid proof-of-stake data
        return True

    # --- This function defines which validator can be selected as forger
    def check_stake(self, block):
        # --- Verify the proof-of-stake data in the block based on the validator's stake and age of coins
        max_age = 1  # --- Maximum age of coins allowed for staking (e.g. 1 second)
        maturity = int(self.env.now - block.timestamp)  # --- Age of the coins being staked
        time_factor = 1 - min(maturity / max_age, 1)  # --- Stake age factor in range [0, 1]

        # --- Check if denominator is zero
        if sum(validator.stake for validator in self.peers) == 0:
            return False

        # --- Verify the proof-of-stake data based on the validator's stake
        block_hash = block.hash
        threshold = (self.stake / sum(validator.stake for validator in self.peers)) * time_factor
        return int(block_hash, 16) / int("f" * 64, 16) <= threshold


# --- This class is used for blockchain and it stores blocks
class Blockchain:
    # --- This function can defines chain
    def __init__(self):
        self.chain = []

    # --- This function create genesis blocks
    def create_genesis_block(self):
        return Block(0, "01/01/2023", "Genesis block", "0")

    # --- This function get last block
    def get_last_block(self):
        if len(self.chain) > 0:
            return self.chain[-1]
        else:
            # --- Handle the case when the chain is empty
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


# --- This class defines our network of blockchain
class Network:
    # --- This function initialize the network
    def __init__(self, num_validators):
        self.stakers = {}
        self.env = simpy.Environment()
        self.blockchain = Blockchain()
        self.validators = [
            Validator(self.env, f"Validator {i}", random.randint(1, 10), self.blockchain, f"Address Node {i}") for i in
            range(num_validators)]
        self.add_connections()

    # --- This function make connections between nodes
    def add_connections(self):
        # --- Connect validators in a mesh network
        for i in range(len(self.validators)):
            for j in range(i + 1, len(self.validators) + 1):
                self.validators[i].add_peer(self.validators[j - 1])
                self.validators[j - 1].add_peer(self.validators[i])

    # --- This function simulate our consensus algorithm and calculate the Fault
    def simulate(self, num_blocks):

        start_time = time.time()

        # --- Create and schedule the arrival of new blocks
        for i in range(num_blocks):
            self.env.process(self.arrive_block(i + 1))

        # --- Run the simulation
        self.env.run()

        # --- Create a file that contain of blocks
        f = open("SHA256/Fault_Tolerance(SHA256)_Blockchain.json", "a")
        f.write(json.dumps(json.loads(jsonpickle.encode(self.blockchain.chain)), indent=2))
        f.close()

    # --- This function make a random string
    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_string = ''.join(random.choice(letters) for i in range(length))
        return result_string

    def arrive_block(self, index):
        # --- Simulate the arrival of new blocks and their processing by validators
        block = Block(index, time.time(), f"Block data {index}", "")
        block.nonce = random.randint(0, 1000)  # --- Assign a random nonce value

        # --- In this part we will use Proof Of stake to select a forger
        pos = ProofOfStake()
        for validator in self.validators:
            pos.update(validator.name, validator.stake)

        # --- When a forger selected it goes to validate the block and then put it to the chain
        forger = pos.forger(self.get_random_string(index))
        for validator in self.validators:
            # --- In here we check which one of validators is forger
            if forger == validator.name:
                validator_node = validator

        yield self.env.process(self.process_block(validator_node, block))

    def process_block(self, validator, block):
        # --- Simulate the validation of blocks by validators
        # sim_time = random.random()
        sim_time = 0.5
        yield self.env.timeout(sim_time)  # --- Simulate some delay
        validator.receive_block(block)  # --- Process the block and propagate to peers

    # --- This function calculates a threshold for fault tolerance
    def calculate_fault_tolerance(self):
        # --- Sort by stake in descending order
        self.validators.sort(key=lambda x: -x.stake)
        total_nodes = len(self.validators)
        faulty_nodes = 0
        stake_sum = sum(v.stake for v in self.validators)
        for i in range(total_nodes):
            if self.validators[i].stake * (total_nodes - i) < stake_sum:
                faulty_nodes += 1

        # --- Calculate fault tolerance
        threshold = stake_sum / total_nodes
        not_faulty_nodes = total_nodes - faulty_nodes
        fault_tolerance = not_faulty_nodes / total_nodes
        return fault_tolerance


def main():
    file1 = open('input.txt', 'r')
    lines1 = file1.readlines()
    metrics = []
    for line in lines1:
        metrics.append(int(line.strip()))
    # --- Number of validators
    num_validators = metrics[0]
    # --- Number of blocks
    num_blocks = metrics[1]
    # ---
    if exists('SHA256/fault_sha256.txt'):
        os.remove('SHA256/fault_sha256.txt')
    if exists('SHA256/Fault_Tolerance(SHA256)_Blockchain.json'):
        os.remove('SHA256/Fault_Tolerance(SHA256)_Blockchain.json')
    # ---
    network = Network(num_validators)
    network.simulate(num_blocks)
    fault_tolerance = network.calculate_fault_tolerance()
    with open('SHA256/fault_sha256.txt', 'a') as the_file:
        the_file.write(f'{fault_tolerance * 100}\n')
    the_file.close()
    print("Processing . . . ")
    time.sleep(2)
    print(f"Fault tolerance: {fault_tolerance * 100} %")


if __name__ == "__main__":
    main()
