import time
import json
from web3 import Web3

ETH_RPC_URL = "http://127.0.0.1:7545"

eth_rpc_url = ETH_RPC_URL
web3 = Web3(Web3.HTTPProvider(eth_rpc_url))

filename = 'abi/contract_reputation.json'

with open(filename, 'r') as f:
    json_data = json.load(f)

contract_name = json_data["contractName"]
abi = json_data["abi"]

contract_address = "0x95B6e766E5ef93935726771d5b2D66A9C3F55c52"

current_time = int(round(time.time() * 1000))

web3.eth.defaultAccount = web3.eth.accounts[0]

contract_ins = web3.eth.contract(
    abi=abi,
    address=web3.toChecksumAddress(contract_address),
)

address = web3.eth.accounts[5]

print('mediator value: {}'.format(
    contract_ins.caller.get_mediator()
))

# print('----------------')
# contract_ins.functions.issue_doctor(
#     _address=address,
#     _email='catedt@gmail.com',
#     _date_created=current_time).transact()
# print('----------------')
#
# print('issued_doctor_state: {}'.format(
#     contract_ins.caller.issued_doctor_state(_address=address)
# ))
#
# # step1
# contract_ins.functions.issue_doctor_repute_center_scoring(_address=address,
#                                                           _has_check_identity=True,
#                                                           _has_career_posting=True,
#                                                           _has_post_specialization=True).transact()

print('get_p_center_score: {}'.format(
    contract_ins.caller.get_p_center_score(_address=address)
))

print('issued_doctor_state: {}'.format(
    contract_ins.caller.issued_doctor_state(_address=address)
))

# # step2
contract_ins.functions.add_increment_repute_customer_scoring(_address=address,
                                                             _complain_count=0,
                                                             _has_not_delay=True,
                                                             _has_regulation_observance=True).transact()

print('issued_doctor_repute: {}'.format(
    contract_ins.caller.issued_doctor_repute(_address=address)
))

print('issued_doctor_state: {}'.format(
    contract_ins.caller.issued_doctor_state(_address=address)

))
