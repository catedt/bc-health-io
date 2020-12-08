import json
import os

import vyper

filename = 'contract/contract_reputation.vy'
contract_name = 'contract_reputation'
contract_json_file = open('abi/contract_reputation.json', 'w')

with open(filename, 'r') as f:
    content = f.read()

current_directory = os.curdir

smart_contract = {current_directory: content}

contract_format = ['abi', 'bytecode']
compiled_code = vyper.compile_codes(smart_contract, contract_format, 'dict')

smart_contract_json = {
    'contractName': contract_name,
    'abi': compiled_code[current_directory]['abi'],
    'byte_code': compiled_code[current_directory]['bytecode']
}

json.dump(smart_contract_json, contract_json_file)

contract_json_file.close()

