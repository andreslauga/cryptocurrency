import hashlib
import datetime
import json
import pprint
from time import time

class Block:

    # Constructor
    def __init__(self, timestamp, transaction, prevoiusBlock = ''):
        self.timestamp = timestamp
        self.transaction = transaction
        self.prevoiusBlock = prevoiusBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(transaction, timestamp, self.difficultyIncrement)
    
    # Calculate Hash function
    def calculateHash(self, data, timestamp, difficultyIncrement):
        data = str(data) + str(timestamp) + str(difficultyIncrement)
        data = data.encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()

    # Block Mining function
    def mineBlock(self, difficulty):
        difficultyCheck = "0" * difficulty
        while self.hash[:difficulty] != difficultyCheck:
            self.hash = self.calculateHash(self.transaction, self.timestamp, self.difficultyIncrement)
            self.difficultyIncrement += 1


class Blockchain:

    # Constructor
    def __init__(self):
        self.chain = [self.GenesisBlock()]
        self.difficulty = 5
        self.pendingTransactions = []
        self.reward = 10
    
    # Returns the first block of the chain
    def GenesisBlock(self):
        genesisBlock = Block(str(datetime.datetime.now()), "I'm the first block of the chain")
        return genesisBlock

    # Returns the last block of the chain
    def getLastBlock(self):
        return self.chain[-1] # [-1] returns the last item of a given array

    # Puts pending transactions into a block and then add the block into the chain
    def minePendingTransaction(self, minerRewardAddress):
        newBlock = Block(str(datetime.datetime.now()), self.pendingTransactions)
        newBlock.mineBlock(self.difficulty)
        newBlock.prevoiusBlock = self.getLastBlock().hash
        print(f"Hash of the previous block: {newBlock.prevoiusBlock}")
        testChain = []
        for transaction in newBlock.transaction:
            temp = json.dumps(transaction.__dict__, indent = 5, separators = (',', ':'))
            testChain.append(temp)
        pprint.pprint(testChain)
        self.chain.append(newBlock)
        print(f"Hash of the current block: {newBlock.hash}")
        print("New block added!")
        rewardTrans = Transaction("System", minerRewardAddress, self.reward)
        self.pendingTransactions.append(rewardTrans)
        self.pendingTransactions = []
    
    # Chain validation
    def isChainValid(self):
        for x in range(1, len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[ x - 1 ]
            if (currentBlock.prevoiusBlock != previousBlock.hash):
                print("Invalid Chain")
        print("The Chain is valid and safe!")

    # Add the transaction into de pool 
    def createTransaction(self, transaction):
        self.pendingTransactions.append(transaction)

    # Returns account balance from given account 
    def getBalance(self, walletAddress):
        balance = 0
        for block in self.chain:
            if block.prevoiusBlock == "":
                continue
            for transaction in block.transaction:
                if transaction.fromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.toWallet == walletAddress:
                    balance += transaction.amount
        return balance

class Transaction:
    
    # Constructor
    def __init__(self, fromWallet, toWallet, amount):
        self.fromWallet = fromWallet
        self.toWallet = toWallet
        self.amount = amount



# --------------- Testing the code ----------------------

my_crypto = Blockchain()

print("Andrés starts mining...")

my_crypto.createTransaction(Transaction("UserA", "UserB", 0.01))
my_crypto.createTransaction(Transaction("UserC", "UserD", 0.46))
my_crypto.createTransaction(Transaction("UserE", "UserF", 2.00))

tiempo_inicio = time()
my_crypto.minePendingTransaction("AndresWalletAddress")
tiempo_final = time()
print(f"Tansaction took { tiempo_final - tiempo_inicio } seconds")

print("-------------------------------------------------------------------------------------")

print("John starts mining...")

my_crypto.createTransaction(Transaction("UserG", "UserH", 0.51))
my_crypto.createTransaction(Transaction("UserI", "UserJ", 146))
my_crypto.createTransaction(Transaction("UserK", "UserL", 7.80))

tiempo_inicio = time()
my_crypto.minePendingTransaction("JohnWalletAddress")
tiempo_final = time()
print(f"Tansaction took { tiempo_final - tiempo_inicio } seconds")

print("-------------------------------------------------------------------------------------")

print("Julia starts mining...")

my_crypto.createTransaction(Transaction("UserL", "UserM", 5.59))
my_crypto.createTransaction(Transaction("UserN", "UserO", 0.16))
my_crypto.createTransaction(Transaction("UserP", "UserQ", 40.0))

tiempo_inicio = time()
my_crypto.minePendingTransaction("JuliaWalletAddress")
tiempo_final = time()
print(f"Tansaction took { tiempo_final - tiempo_inicio } seconds")

print("-------------------------------------------------------------------------------------")

print("Andrés has " + str(my_crypto.getBalance("AndresWalletAddress")) + " andycoins in his wallet")
print("John has " + str(my_crypto.getBalance("JohnWalletAddress")) + " andycoins in his wallet")
print("Julia has " + str(my_crypto.getBalance("JuliaWalletAddress")) + " andycoins in her wallet")

print("-------------------------------------------------------------------------------------")

# Blockchain hashes
for x in range(len(my_crypto.chain)):
    print(f"Hash del bloque {x}: {my_crypto.chain[x].hash}")

print(my_crypto.isChainValid())