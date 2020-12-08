import time

from django.conf import settings
from web3 import Web3

from main.models import Doctor


class EthReputation:
    eth_rpc_url = settings.ETH_RPC_URL

    def __init__(self, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(self.eth_rpc_url))

        # self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        self.contract_ins = self.web3.eth.contract(
            abi=abi,
            address=self.web3.toChecksumAddress(contract_address),
        )

    def __str__(self):
        return self.eth_rpc_url

    def issue_doctor(self, address, email):
        current_time = int(round(time.time() * 1000))

        self.contract_ins.functions.issue_doctor(
            _address=self.web3.toChecksumAddress(address),
            _email=email,
            _date_created=current_time).transact()

        print('mediator value: {}'.format(
            self.contract_ins.caller.get_mediator()
        ))

        print('issued_doctor_state: {}'.format(
            self.contract_ins.caller.issued_doctor_state(_address=address)
        ))

    def issue_doctor_repute_center_scoring(self, address, has_check_identity, has_career_posting,
                                           has_post_specialization):
        # # step1
        self.contract_ins.functions.issue_doctor_repute_center_scoring(
            _address=address,
            _has_check_identity=has_check_identity,
            _has_career_posting=has_career_posting,
            _has_post_specialization=has_post_specialization).transact()

        print('get_p_center_score: {}'.format(
            self.contract_ins.caller.get_p_center_score(_address=address)
        ))

    def issue_doctor_repute_customer_scoring(self, address, complain_count, has_not_delay,
                                             has_regulation_observance):
        # # step2
        self.contract_ins.functions.add_increment_repute_customer_scoring(
            _address=address,
            _complain_count=complain_count,
            _has_not_delay=has_not_delay,
            _has_regulation_observance=has_regulation_observance).transact()

        print('repute: {}'.format(
            self.contract_ins.caller.issued_doctor_repute(_address=address)
        ))

    def issued_doctor_repute(self, address):
        return self.contract_ins.caller.issued_doctor_repute(_address=self.web3.toChecksumAddress(address))

    def issued_doctor_state(self, address):
        return self.contract_ins.caller.issued_doctor_state(_address=self.web3.toChecksumAddress(address))
