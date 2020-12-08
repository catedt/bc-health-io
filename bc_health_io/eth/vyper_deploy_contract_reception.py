import json
from web3 import Web3

ETH_RPC_URL = "http://127.0.0.1:7545"

eth_rpc_url = ETH_RPC_URL
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))

filename = 'abi/contract_reception.json'

with open(filename, 'r') as f:
    json_data = json.load(f)

contract_name = json_data["contractName"]
abi = json_data["abi"]
byte_code = json_data["byte_code"]

web3.eth.defaultAccount = web3.eth.accounts[0]

print('UNLOCK ACCOUNT {}'.format(
    web3.geth.personal.unlock_account(web3.eth.accounts[0], "catedt", None),
))


def deploy_contract(w3, deploy_abi, deploy_byte_code):
    deploy_tx_hash = w3.eth.contract(
        abi=deploy_abi,
        bytecode=deploy_byte_code).constructor(web3.eth.accounts[1],
                                               Web3.toWei(4, 'ether'),
                                               Web3.toWei(2, 'ether')).transact()

    print('deploy_tx_hash value: {}'.format(
        deploy_tx_hash
    ))

    deploy_tx_receipt = w3.eth.waitForTransactionReceipt(deploy_tx_hash)
    return deploy_tx_receipt


tx_receipt = deploy_contract(web3, abi, byte_code)

print('contract value: {}\n, abi: {},\n byte_code: {}'.format(
    abi,
    byte_code,
    web3.toChecksumAddress(tx_receipt.contractAddress),
))

