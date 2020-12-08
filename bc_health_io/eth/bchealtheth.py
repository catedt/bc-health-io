from django.conf import settings
from web3 import Web3
from web3.auto.infura import w3


class BcHealthEth:
    eth_rpc_url = "https://ropsten.infura.io/v3/a84c416fba01474785187e01118c4eea"

    # eth_rpc_url = settings.ETH_RPC_URL
    web3 = Web3(Web3.HTTPProvider(eth_rpc_url))

    peer_address = "0x4c11a637D0ded81Dd7ee74944401259ef531Ed29"

    def __str__(self):
        return self.eth_rpc_url

    def get_balance(self, peer_address):
        return self.web3.eth.getBalance(peer_address)


bhe = BcHealthEth()
print(bhe.get_balance(bhe.peer_address))
