import hashlib
import json
from time import time
from urllib.parse import urlparse

import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)
        self.nodes = set()

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        for i, block in enumerate(chain):
            if i == 0:
                continue
            last_block_hash_check = self.hash(last_block) == block[
                'previous_hash']
            proof_check = self.valid_proof(last_block['proof'], block['proof'])
            if not (last_block_hash_check and proof_check):
                return False
            last_block = block

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash=None):
        # Creates a new Block and adds it to the chain
        if previous_hash is None:
            previous_hash = self.hash(self.chain[-1])

        block = dict(
            index=len(self.chain) + 1,
            timestamp=time(),
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash)

        # reset the current transactions
        self.current_transactions = []

        # append the block
        self.chain.append(block)
        return block

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def proof_of_work(self, last_proof):

        proof = 0
        while self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = '{}{}'.format(last_proof, proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == '0000'

    def new_transaction(self, sender, recipient, amount):
        """
        Add a transaction

        Returns:
        The index of the block the transition has to be added to.
        """
        trans = dict(sender=sender, recipient=recipient, amount=amount)
        self.current_transactions.append(trans)
        return self.chain[-1]['index'] + 1

    @staticmethod
    def hash(block):
        # Hashes a Block

        block_jsonstr = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_jsonstr).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]
