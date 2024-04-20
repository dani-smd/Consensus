import csv
import sys
import random
import string


class Transaction:
    def __init__(self, tx_id, sender, recipient, amount):
        self.tx_id = tx_id
        self.sender = sender
        self.recipient = recipient
        self.amount = amount


def generate_transaction(tx_id):
    sender = ''.join(random.choices(string.ascii_letters, k=42))  # Random sender name
    recipient = ''.join(random.choices(string.ascii_letters, k=42))  # Random recipient name
    amount = random.randint(1, 100)  # Random transaction amount
    return Transaction(tx_id, sender, recipient, amount)


def generate_transaction_pool(size):
    transaction_pool = []
    for i in range(size):
        transaction_pool.append(generate_transaction(i))
    return transaction_pool


def export_transaction_pool_to_csv(transaction_pool, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Transaction ID', 'Sender', 'Recipient', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for transaction in transaction_pool:
            writer.writerow({'Transaction ID': transaction.tx_id,
                             'Sender': transaction.sender,
                             'Recipient': transaction.recipient,
                             'Amount': transaction.amount})


# Example usage
if __name__ == "__main__":
    # Check if the user provided a command-line argument for the number of transactions
    if len(sys.argv) != 2:
        print("Usage: python transaction_pool.py <number_of_transactions>")
        sys.exit(1)

    # Get the number of transactions from the command-line argument
    try:
        num_transactions = int(sys.argv[1])
    except ValueError:
        print("Number of transactions must be an integer")
        sys.exit(1)

    # Generate a transaction pool with the specified number of transactions
    transaction_pool = generate_transaction_pool(num_transactions)

    # Export transaction pool to a CSV file
    export_transaction_pool_to_csv(transaction_pool, 'transaction_pool.csv')

    print("Transaction pool dataset generated and exported to 'transaction_pool.csv'")
