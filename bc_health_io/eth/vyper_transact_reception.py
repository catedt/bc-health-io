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

contract_address = "0x2A8D743d9f579671AAA54242256a48E7cfD4e12D"

web3.eth.defaultAccount = web3.eth.accounts[0]

contract_ins = web3.eth.contract(
    abi=abi,
    address=web3.toChecksumAddress(contract_address),
)

print('current value: mediator {}, receptionist {}'.format(
    contract_ins.caller.get_mediator(), contract_ins.caller.get_receptionist()
))

print('accounts: account1 {}, account2 {}, account3 {}'.format(
    web3.eth.accounts[0],
    web3.eth.accounts[1],
    web3.eth.accounts[2],
))

print('UNLOCK ACCOUNT {}'.format(
    web3.geth.personal.unlock_account(web3.eth.accounts[0], "catedt", None),
))

print('member: mediator {}, receptionist {}, adopter {}'.format(
    contract_ins.caller.get_mediator(),
    contract_ins.caller.get_receptionist(),
    contract_ins.caller.get_adopter(),
))

web3.eth.defaultAccount = web3.eth.accounts[1]

contract_ins.functions.reception().transact(dict({"from": web3.eth.accounts[1], "value": web3.toWei(6, 'ether')}))

print('reception_started value: {}'.format(
   contract_ins.caller.is_reception_started()
))
web3.eth.defaultAccount = web3.eth.accounts[2]

contract_ins.functions.adopt_reception().transact(dict({"from": web3.eth.accounts[2], "value": web3.toWei(2, 'ether')}))

print('balance3: mediator {}, receptionist {}, adopter {}'.format(
    web3.eth.getBalance(web3.eth.accounts[0]),
    web3.eth.getBalance(web3.eth.accounts[1]),
    web3.eth.getBalance(web3.eth.accounts[2]),
))
print('adopted value: {}'.format(
   contract_ins.caller.is_adopted()
))

contract_ins.functions.opinion_received().transact()

print('received: {}, {}'.format(
    contract_ins.caller.get_received_count(),
    contract_ins.caller.is_received()
))

web3.eth.defaultAccount = web3.eth.accounts[1]
contract_ins.functions.opinion_complained().transact()

print('opinion complained : {}'.format(
    contract_ins.caller.is_complained()
))

web3.eth.defaultAccount = web3.eth.accounts[2]
contract_ins.functions.opinion_received().transact()

print('received: {}, {}'.format(
    contract_ins.caller.get_received_count(),
    contract_ins.caller.is_received()
))


web3.eth.defaultAccount = web3.eth.accounts[1]
contract_ins.functions.opinion_confirmed().transact()

# print('opinion confirmed : {}'.format(
#     contract_ins.caller.is_confirmed()
# ))

print('fin. accounts: account1 {}, account2 {}, account3 {}'.format(
    web3.eth.accounts[0],
    web3.eth.accounts[1],
    web3.eth.accounts[2],
))

print('balance3: mediator {}, receptionist {}, adopter {}'.format(
    web3.eth.getBalance(web3.eth.accounts[0]),
    web3.eth.getBalance(web3.eth.accounts[1]),
    web3.eth.getBalance(web3.eth.accounts[2]),
))