from os.path import exists
import jsonpickle
import string
import random
import simpy
import time
import json
import os

from blake.library.blockchain import Blockchain
from blake.library.vlidator import Validator
from blake.library.ProofOfStake import ProofOfStake
from blake.library.block import Block


# --- This class defines our network.py of blockchain
class Network:
    # --- This function initialize the network.py
    def __init__(self, num_validators):
        self.env = simpy.Environment()
        self.blockchain = Blockchain()
        self.validators = [
            Validator(self.env, f"Validator {i}", random.randint(1, 10), self.blockchain, f"Address Node {i}") for i in
            range(num_validators)]
        self.num_validators = num_validators
        self.add_connections()

    # --- This function make connections between nodes
    def add_connections(self):
        # --- Connect validators in a mesh network.py
        for i in range(len(self.validators)):
            for j in range(i + 1, len(self.validators)):
                self.validators[i].add_peer(self.validators[j])
                self.validators[j].add_peer(self.validators[i])

    # --- This function simulate our consensus algorithm and calculate the Latency
    def simulate(self, num_blocks, status):
        start_time = time.time()

        # --- Create and schedule the arrival of new blocks
        for i in range(num_blocks):
            self.env.process(self.arrive_block(i + 1))

        # --- Run the simulation
        self.env.run()

        end_time = time.time()

        elapsed_time = end_time - start_time

        processed_blocks = len(self.blockchain.chain)

        throughput = processed_blocks / elapsed_time

        with open('blake/files/throughput.txt', 'a') as the_file:
            the_file.write(f'{throughput:.6f}\n')
        the_file.close()

        if status:
            f = open("blake/files/Throughput(blake)_Blockchain.json", "a")
            f.write(json.dumps(json.loads(jsonpickle.encode(self.blockchain.chain)), indent=2))
            f.close()

    # --- This function make a random string
    @staticmethod
    def get_random_string(length):
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
        num_simulations = 10
        forger = pos.monte_carlo_forger(num_simulations, self.get_random_string(index))

        for validator in self.validators:
            # --- In here we check which one of validators is forger
            if forger == validator.name:
                yield self.env.process(self.process_block(validator, block))

    def process_block(self, validator, block):
        # --- Simulate the validation of blocks by validators
        sim_time = 0.5
        yield self.env.timeout(sim_time)  # --- Simulate some delay
        validator.receive_block(block)  # --- Process the block and propagate to peers
