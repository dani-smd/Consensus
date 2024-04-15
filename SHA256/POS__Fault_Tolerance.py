from os.path import exists
import jsonpickle
import random
import string
import simpy
import json
import time
import os

from Library.blockchain import Blockchain
from Library.vlidator import Validator
from SHA256.Library.ProofOfStake import ProofOfStake
from Library.block import Block


# --- This class defines our network.py of blockchain
class Network:
    # --- This function initialize the network.py
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
        # --- Connect validators in a mesh network.py
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
        forger = pos.forger(self.get_random_string(index))
        for validator in self.validators:
            # --- In here we check which one of validators is forger
            if forger == validator.name:
                yield self.env.process(self.process_block(validator, block))

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
        sorted_validators = sorted(self.validators, key=lambda v: v.stake, reverse=True)
        stake_sum = sum(v.stake for v in self.validators)
        # for i in range(total_nodes):
        #     if self.validators[i].stake * (total_nodes - i) < stake_sum:
        #         faulty_nodes += 1
        faulty_nodes = 0
        cumulative_stake = 0
        for i, validator in enumerate(sorted_validators):
            cumulative_stake += validator.stake
            if cumulative_stake >= stake_sum * 0.3:
                faulty_nodes = i + 1
                break

        # --- Calculate fault tolerance
        not_faulty_nodes = total_nodes - faulty_nodes
        fault_tolerance = not_faulty_nodes / total_nodes
        f = (2 * faulty_nodes) + 1
        return fault_tolerance, f


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
    fault_tolerance, f = network.calculate_fault_tolerance()
    with open('SHA256/fault_sha256.txt', 'a') as the_file:
        the_file.write(f'{fault_tolerance * 100}\n')
    the_file.close()
    print("Processing . . . ")
    time.sleep(2)
    print(f"Fault tolerance: {fault_tolerance * 100} %")
    print(f"The Result Of 2F+1 Is Equal = {f}, It Means you Need At Least {f} Node For The POS Consensus To Work!")


if __name__ == "__main__":
    main()
