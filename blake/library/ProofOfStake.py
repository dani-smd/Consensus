import random
from blake.library.Lot import Lot
from blake.library.BlockchainUtils import BlockChainUtils


class ProofOfStake():

    def __init__(self):
        self.stakers = {}

    def update(self, publicKeyString, stake):
        if publicKeyString in self.stakers.keys():
            self.stakers[publicKeyString] += stake
        else:
            self.stakers[publicKeyString] = stake
        
    def get(self, publicKeyString):
        if publicKeyString in self.stakers.keys():
            return self.stakers[publicKeyString]
        else:
            return None
    
    def validatorLots(self, seed):
        lots = []
        for validator in self.stakers.keys():
            for stake in range(self.get(validator)):
                lots.append(Lot(validator, stake+1, seed))
        return lots
    
    def winnerLot(self, lots, seed):
        winnerLot = None
        leastOffset = None
        referenceHashIntValue = int(BlockChainUtils.hash(seed).hexdigest(), 16)
        for lot in lots:
            lotIntValue = int(lot.lotHash(), 16)
            offset = abs(lotIntValue-referenceHashIntValue)
            if leastOffset is None or offset < leastOffset:
                leastOffset = offset
                winnerLot = lot
        return winnerLot
    
    def forger(self, lastBlockHash):
        lots = self.validatorLots(lastBlockHash)
        winnerLot = self.winnerLot(lots, lastBlockHash)
        if winnerLot:
            return winnerLot.publicKey
        else:
            return None

    def monte_carlo_forger(self, num_simulations, lastBlockHash):
        forger_counts = {}
        block_hash = lastBlockHash
        # Run Monte Carlo simulations
        for _ in range(num_simulations):
            forger = self.forger(block_hash)
            if forger:
                if forger in forger_counts:
                    forger_counts[forger] += 1
                else:
                    forger_counts[forger] = 1
