from django.conf import settings
from web3 import Web3


class EthReception:
    eth_rpc_url = settings.ETH_RPC_URL

    def __init__(self, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(self.eth_rpc_url))
        self.web3.eth.defaultAccount = self.web3.eth.accounts[1]
        self.contract_ins = self.web3.eth.contract(
            abi=abi,
            address=self.web3.toChecksumAddress(contract_address),
        )

    def __str__(self):
        return self.eth_rpc_url

    def reception(self, address, value):
        self.contract_ins.functions.reception().transact(
            dict({"from": self.web3.toChecksumAddress(address), "value": self.web3.toWei(value, 'ether')}))

    def is_reception_started(self):
        return self.contract_ins.caller.is_reception_started()

    def adopt_reception(self, address, value):
        self.contract_ins.functions.adopt_reception().transact(
            dict({"from": self.web3.toChecksumAddress(address), "value": self.web3.toWei(2, 'ether')}))

    def is_adopted(self):
        return self.contract_ins.caller.is_adopted()

    def opinion_complained(self):
        self.contract_ins.functions.opinion_complained().transact()

    def is_complained(self):
        return self.contract_ins.caller.is_complained()

    def opinion_received(self):
        self.contract_ins.functions.opinion_received().transact()
