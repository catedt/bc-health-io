from django.conf import settings
import time
import json
from web3 import Web3


class ContractDeploy:

    def __init__(self, eth_rpc_url):
        self.web3 = Web3(Web3.HTTPProvider(eth_rpc_url))
        # self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        # self.web3.geth.personal.unlock_account(self.web3.eth.accounts[0], "catedt", None),
        # self.account = self.web3.eth.account.privateKeyToAccount('713b1927ad9139bdb36225f2f5f375c3c7a51f5589fb6a72c1dc87a07c6bf638')

    def get_deployed_contract_file_path(self, file_path_name):
        with open(file_path_name, 'r') as f:
            json_data = json.load(f)
        return json_data

    def deploy_contract_file_path(self, file_path_name):
        with open(file_path_name, 'r') as f:
            json_data = json.load(f)

            contract_name = json_data["contractName"]
            abi = json_data["abi"]
            byte_code = json_data["byte_code"]

            current_time = int(round(time.time() * 1000))
            deploy_tx_hash = self.web3.eth.contract(
                abi=abi,
                bytecode=byte_code).constructor(current_time).transact()

            print('deploy_tx_hash value: {}'.format(
                deploy_tx_hash
            ))

            deploy_tx_receipt = self.web3.eth.waitForTransactionReceipt(deploy_tx_hash)

            if deploy_tx_receipt:
                address = self.web3.toChecksumAddress(deploy_tx_receipt.contractAddress)
                print('deployed value: {}, {}'.format(
                    address,
                    contract_name
                ))
                contract_result = {'contract_name': contract_name, 'abi': abi,
                                   'byte_code': byte_code, 'contract_address': address}
                return contract_result

    def deploy_contract_file_path_with_eth(self, file_path_name, receptionist_address, cost, fee):
        with open(file_path_name, 'r') as f:
            json_data = json.load(f)

            contract_name = json_data["contractName"]
            abi = json_data["abi"]
            byte_code = json_data["byte_code"]

            print('UNLOCK ACCOUNT {}'.format(
                self.web3.geth.personal.unlock_account(receptionist_address,
                                                       "catedt", None),
            ))

            deploy_tx_hash = self.web3.eth.contract(
                abi=abi,
                bytecode=byte_code).constructor(receptionist_address,
                                                Web3.toWei(cost, 'ether'),
                                                Web3.toWei(fee, 'ether')).transact()

            print('deploy_tx_hash value: {}'.format(
                deploy_tx_hash
            ))

            deploy_tx_receipt = self.web3.eth.waitForTransactionReceipt(deploy_tx_hash)

            if deploy_tx_receipt:
                address = self.web3.toChecksumAddress(deploy_tx_receipt.contractAddress)
                print('deployed value: {}, {}'.format(
                    address,
                    contract_name
                ))
                contract_result = {'contract_name': contract_name, 'abi': abi,
                                   'byte_code': byte_code, 'contract_address': address}
                return contract_result

# tx_receipt = deploy_contract(web3, abi, byte_code)
# ETH_RPC_URL = "http://127.0.0.1:7545"
#
# ct_result = ContractDeploy(ETH_RPC_URL).deploy_contract_file_path('abi/contract_reputation.json')
#
# print('deployed contract value: {}\n, abi: {},\n byte_code: {}'.format(
#     ct_result['abi'],
#     ct_result['byte_code'],
#     ct_result['contract_address'],
# ))
