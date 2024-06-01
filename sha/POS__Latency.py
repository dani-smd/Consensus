import jsonpickle
import random
import string
import simpy
import json
import time
import csv

from sha.library.blockchain import Blockchain
from sha.library.vlidator import Validator
from sha.library.ProofOfStake import ProofOfStake
from sha.library.block import Block


class Transaction:
    def __init__(self, tx_id, sender, recipient, amount):
        self.tx_id = tx_id
        self.sender = sender
        self.recipient = recipient
        self.amount = amount


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

    # --- This function simulate our consensus algorithm and calculate the Latency
    def simulate(self, num_blocks, status):
        start_time = time.time()

        # --- Create and schedule the arrival of new blocks
        for i in range(num_blocks):
            self.env.process(self.arrive_block(i + 1))

        # --- Run the simulation
        self.env.run()

        end_time = time.time()

        latency = (end_time - start_time) / num_blocks

        with open('sha/files/latency.txt', 'a') as the_file:
            the_file.write(f'{latency:.6f}\n')
        the_file.close()

        if status:
            f = open("sha/files/Latency(sha)_Blockchain.json", "a")
            f.write(json.dumps(json.loads(jsonpickle.encode(self.blockchain.chain)), indent=2))
            f.close()

    # --- This function make a random string
    @staticmethod
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_string = ''.join(random.choice(letters) for i in range(length))
        return result_string

    @staticmethod
    def read_transactions_from_csv():
        transaction_pool = []
        with open('transaction_pool.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                transaction = Transaction(
                    int(row['Transaction ID']),
                    row['Sender'],
                    row['Recipient'],
                    int(row['Amount'])
                )
                transaction_pool.append(transaction)
        return transaction_pool

    def arrive_block(self, index):
        transaction_pool = self.read_transactions_from_csv()
        selected_transactions = random.sample(transaction_pool, 10)
        # --- Simulate the arrival of new blocks and their processing by validators
        block = Block(index, time.time(), selected_transactions, "")
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
                # --- Check how many times a validator selected as a forger
                if validator.name in self.stakers.keys():
                    self.stakers[validator.name] += 1
                else:
                    self.stakers[validator.name] = 1

    def process_block(self, validator, block):
        # --- Simulate the validation of blocks by validators
        # sim_time = random.random()
        sim_time = 0.5
        yield self.env.timeout(sim_time)  # --- Simulate some delay
        validator.receive_block(block)  # --- Process the block and propagate to peers
