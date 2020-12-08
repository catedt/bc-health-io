from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from eth.eth_deploy_contract import ContractDeploy
from eth.eth_reputation import EthReputation
from main.models import DeployedContract
from reputation.forms import ReputationForm
from reputation.models import Reputation


def index(request):
    latest_data_list = Reputation.objects.all().order_by('-updateDate')[:5]
    context = {'latest_data_list': latest_data_list}
    return render(request, 'reputation/index.html', context)


def detail(request, data_id):
    data_info = Reputation.objects.get(doctorId=data_id)
    print(data_info)

    json_data = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path('eth/abi/contract_reputation.json')

    data = DeployedContract.objects.filter(contractName='contract_reputation').order_by('-id').first()
    print(data.contractAddress)

    doctor_id = data_id
    contract_address = data.contractAddress
    abi = json_data['abi']

    eth = EthReputation(contract_address=contract_address, abi=abi)
    repute = eth.issued_doctor_repute(doctor_id)
    state = eth.issued_doctor_state(doctor_id)

    data = {"repute": repute, "contractAddress": contract_address, 'state': state}

    context = {'reputation_data': data_info, 'transact_data': data}

    return render(request, 'reputation/detail.html', context)


def mod(request, data_id):
    print('mode enter')
    if request.method == 'POST':
        form = ReputationForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            if 'new' == data_id:
                form.save(commit=True)
            else:
                reputation_info = Reputation.objects.get(rid=data_id)
                if reputation_info:
                    reputation_info.doctorId = cleaned['adopterId']
                    reputation_info.email = cleaned['email']
                    reputation_info.repute = cleaned['repute']
                    reputation_info.createDate = cleaned['createDate']
                    reputation_info.updateDate = cleaned['updateDate']

                    reputation_info.save()

            return HttpResponseRedirect(reverse('reputation'))
    else:
        if 'new' == data_id:
            reputation_info = Reputation()
        else:
            reputation_info = Reputation.objects.get(rid=data_id)
        form = ReputationForm(instance=reputation_info)
        context = {'block_data': reputation_info, 'data_id': data_id, 'form': form}
        return render(request, 'reputation/write.html', context)
