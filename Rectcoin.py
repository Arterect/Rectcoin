"""
Author: Hayate Esaki by Arterect
Date: 2023/07/01
Description: Rectcoin Deployment Code

"""

import json, solcx
from web3 import Web3
from solcx import compile_files
from eth_account import Account

# Ganache connection information
url = "Ganache_local_network" # Set the appropriate value in the Ganache URL
web3 = Web3(Web3.HTTPProvider(url))

# Read coin information from JSON file
coin_info_file = "Rectcoin.json"
with open(coin_info_file, 'r') as f:
    coin_info = json.load(f)

name = coin_info["name"]
symbol = coin_info["symbol"]
initial_supply = coin_info["initial_supply"]

# Path of smart contract source code file
contract_file_path = "contracts/Rectcoin.sol"
contract_name = "Rectcoin"

# Compile
solcx.set_solc_version('0.8.0')
compiled_contracts = compile_files([contract_file_path])

# Key to the contract
contract_key = f"{contract_file_path}:{contract_name}"

# Get byte code and ABI
contract_bytecode = compiled_contracts[contract_key]["bin"]
contract_abi = compiled_contracts[contract_key]["abi"]

# Deploy smart contract
contract = web3.eth.contract(bytecode=contract_bytecode, abi=contract_abi)

# Set up your account
private_key = "your_private_key" # Set the appropriate private key
account = Account.from_key(private_key)
account_address = account.address

constructor_arguments = [name, symbol, initial_supply]

transaction = contract.constructor(*constructor_arguments).build_transaction({
    'from': account_address,
    'nonce': web3.eth.get_transaction_count(account_address),
    'gas': 2000000,
    'gasPrice': web3.eth.gas_price
})

# Sign the transaction
signed_transaction = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send transaction
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Waiting for transaction mining
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

# Get address of deployed contract
contract_address = transaction_receipt["contractAddress"]

# Create an instance of the contract
deployed_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function calls for contracts
name = deployed_contract.functions.name().call()
symbol = deployed_contract.functions.symbol().call()
total_supply = deployed_contract.functions.totalSupply().call()

# Deployment Confirmation
print("Crypto asset name:", name)
print("symbol:", symbol)
print("total supply:", total_supply)
print("ERC20 token deployed at address:", contract_address)
print("contract_bytecode:", contract_bytecode)
print("contract_abi:", contract_abi)
