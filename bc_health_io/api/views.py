from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.utils.datetime_safe import time
from rest_framework import viewsets, renderers, status, mixins, generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from eth.eth_deploy_contract import ContractDeploy

from api.serializers import UserSerializer, GroupSerializer, HbBlockDataSerializer, DoctorSerializer, ClientSerializer, \
    ReputationSerializer, MediatorSerializer, SmartContractSerializer, ReceptionSerializer, DeployedContractSerializer, \
    DeployedReputationSerializer
from eth.eth_reception import EthReception
from eth.eth_reputation import EthReputation
from main.models import HbBlockData, Doctor, Client, Mediator, SmartContract, Reception, DeployedContract, \
    DeployedContractHistory
from reputation.models import Reputation


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class HbBlockDataSet(viewsets.ModelViewSet):
    """
    API endpint that allows HbBlockDataSet
    """
    queryset = HbBlockData.objects.all()
    serializer_class = HbBlockDataSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDataSet(viewsets.ModelViewSet):
    """
    API endpint that allows Doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientDataSet(viewsets.ModelViewSet):
    """
    API endpint that allows Client
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class MediatorDataSet(viewsets.ModelViewSet):
    """
    API endpint that allows Mediator
    """
    queryset = Mediator.objects.all()
    serializer_class = MediatorSerializer
    permission_classes = [permissions.IsAuthenticated]


class SmartContractDataSet(viewsets.ModelViewSet):
    """
    API endpint that allows SmartContract
    """
    queryset = SmartContract.objects.all()
    serializer_class = SmartContractSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReputationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Reputation.objects.all()
    serializer_class = ReputationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        reputation = self.get_object()
        return Response(reputation.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReceptionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Reception.objects.all()
    serializer_class = ReceptionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        reception = self.get_object()
        return Response(reception.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeployReception(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):

    queryset = DeployedContract.objects.filter(contractName='contract_reception')
    serializer_class = DeployedContractSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        receptionist_address = '0x00C9D10718A849c792C59a5fC3587Aaeb911009C'
        cost = '0.001'
        fee = '0.0002'

        ct_result = ContractDeploy(settings.ETH_RPC_URL).deploy_contract_file_path_with_eth(
            'eth/abi/contract_reception.json',
            receptionist_address,
            cost,
            fee)
        print(ct_result)
        if not ct_result:
            serializer = self.get_serializer(data=request.data)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                dc = DeployedContract.objects.filter(contractName=ct_result['contract_name']).order_by('-id').first()
            except ObjectDoesNotExist:
                dc = DeployedContract()

            dc.contractAddress = ct_result['contract_address']
            dc.abi = ct_result['abi']
            dc.contractName = ct_result['contract_name']

            current_time = datetime.now()
            dc.deployDate = current_time.strftime("%Y-%m-%d %H:%M:%S")
            dc.save()

            dch = DeployedContractHistory()
            dch.repute = dc.repute
            dch.deployDate = dc.deployDate
            dch.abi = dc.abi
            dch.contractName = dc.contractName
            dch.contractAddress = dc.contractAddress
            dch.save()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()

            serializer.data['contractAddress'] = dc.contractAddress
            serializer.data['abi'] = dc.abi
            serializer.data['contractName'] = dc.contractName
            serializer.data['deployDate'] = dc.deployDate

        return HttpResponseRedirect(reverse('deploy_reception'))


class DeployReputation(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       generics.GenericAPIView):

    queryset = DeployedContract.objects.filter(contractName='contract_reputation')
    serializer_class = DeployedContractSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        ct_result = ContractDeploy(settings.ETH_RPC_URL).deploy_contract_file_path('eth/abi/contract_reputation.json')
        print(ct_result)
        if not ct_result:
            serializer = self.get_serializer(data=request.data)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            try:
                dc = DeployedContract.objects.filter(contractName=ct_result['contract_name']).order_by('-id').first()
                if not dc:
                    dc = DeployedContract()
            except ObjectDoesNotExist:
                dc = DeployedContract()

            dc.contractAddress = ct_result['contract_address']
            dc.abi = ct_result['abi']
            dc.contractName = ct_result['contract_name']

            current_time = datetime.now()
            dc.deployDate = current_time.strftime("%Y-%m-%d %H:%M:%S")
            dc.save()

            dch = DeployedContractHistory()
            dch.repute = dc.repute
            dch.deployDate = dc.deployDate
            dch.abi = dc.abi
            dch.contractName = dc.contractName
            dch.contractAddress = dc.contractAddress
            dch.save()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid()

            serializer.data['contractAddress'] = dc.contractAddress
            serializer.data['abi'] = dc.abi
            serializer.data['contractName'] = dc.contractName
            serializer.data['deployDate'] = dc.deployDate

        return HttpResponseRedirect(reverse('deploy_reputation'))


class TransactReception(APIView):

    def get(self, request, format=None):
        data = DeployedContract.objects.filter(contractName='contract_reception').latest('deployDate')
        print(data.contractAddress)

        json_data = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path('eth/abi/contract_reception.json')

        contract_address = "0x2A8D743d9f579671AAA54242256a48E7cfD4e12D"
        abi = json_data['abi']

        doctor_id = '0x5d8B7FC8B7c935aDC005856E2c3770c13F63Fb59'

        print('repute up value: {}'.format(
            data.repute
        ))

        serializer = DeployedReputationSerializer(data, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = DeployedContract.objects.filter(contractName='contract_reception').latest('deployDate')
        print(data.contractAddress)
        address = '0x00C9D10718A849c792C59a5fC3587Aaeb911009C'

        ct_result = ContractDeploy(settings.ETH_RPC_URL).deploy_contract_file_path_with_eth('eth/abi/contract_reception.json', address, '2', '1')

        contract_address = ct_result['contract_address']
        abi = ct_result['abi']

        print('reception : {}'.format(
            contract_address
        ))

        return HttpResponseRedirect(reverse('transact_reception'))


class TransactReputationInit(APIView):

    def get(self, request, format=None):
        data = DeployedContract.objects.filter(contractName='contract_reputation').order_by('-id').first()
        print(data.contractAddress)

        json_data = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path('eth/abi/contract_reputation.json')

        contract_address = data.contractAddress
        abi = json_data['abi']

        eth = EthReputation(contract_address=contract_address, abi=abi)
        doctor_id = '0x7492186aA68290c3C7673F782C53C2cbC0609efd'

        data = DeployedContract()
        data.contractName = json_data['contractName']
        data.abi = abi
        data.deployDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.contractAddress = contract_address
        data.repute = eth.issued_doctor_repute(doctor_id)

        print('repute up value: {}'.format(
            data.repute
        ))

        # print(eth.issued_doctor_repute())
        serializer = DeployedReputationSerializer(data, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = DeployedContract.objects.filter(contractName='contract_reputation').order_by('-id').first()
        print(data.contractAddress)

        ct_result = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path(
            'eth/abi/contract_reputation.json')

        doctor_id = '0x686bbC09E7964F77510bC5c43D5fcB7d445D6E5B'
        email = 'catedt@outlook.com'
        contract_address = data.contractAddress
        abi = ct_result['abi']

        eth = EthReputation(contract_address=contract_address, abi=abi)

        _has_check_identity = True
        _has_career_posting = True
        _has_post_specialization = True
        eth.issue_doctor(doctor_id, email)
        eth.issue_doctor_repute_center_scoring(
            doctor_id,
            _has_check_identity,
            _has_career_posting,
            _has_post_specialization)

        repute = eth.issued_doctor_repute(doctor_id)

        try:
            dt = Doctor.objects.filter(ethAddress=doctor_id).order_by('-id').first()
            if dt is not None:
                dt.repute = repute
                dt.email = email
                dt.has_repute = True
                dt.ethAddress = doctor_id
                dt.save()
        except ObjectDoesNotExist:
            dt = Doctor()
            dt.email = email
            dt.has_repute = True
            dt.repute = 0
            dt.ethAddress = doctor_id
            dt.save()

        try:
            rp = Reputation.objects.get(doctorId=doctor_id)
        except ObjectDoesNotExist:
            rp = Reputation()

        print(rp)
        rp.email = email
        rp.repute = repute
        rp.updateDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rp.save()
        return HttpResponseRedirect(reverse('reputation_init'))


class TransactReputationAdd(APIView):

    def get(self, request, *args, **kwargs):
        data = DeployedContract.objects.filter(contractName='contract_reputation').order_by('-id').first()
        print(data.contractAddress)

        json_data = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path('eth/abi/contract_reputation.json')

        doctor_id = '0x686bbC09E7964F77510bC5c43D5fcB7d445D6E5B'
        contract_address = data.contractAddress
        abi = json_data['abi']
        # abi = data.abi

        eth = EthReputation(contract_address=contract_address, abi=abi)

        repute = eth.issued_doctor_repute(doctor_id)
        stat = eth.issued_doctor_state(doctor_id)

        data = Doctor()
        data.email = '-blind-'
        data.repute = repute
        data.status = stat
        data.has_repute = True
        data.ethAddress = doctor_id
        serializer = DoctorSerializer(data, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = DeployedContract.objects.filter(contractName='contract_reputation').order_by('-id').first()
        print(data.contractAddress)

        ct_result = ContractDeploy(settings.ETH_RPC_URL).get_deployed_contract_file_path(
            'eth/abi/contract_reputation.json')

        doctor_id = '0x7492186aA68290c3C7673F782C53C2cbC0609efd'
        contract_address = data.contractAddress
        abi = ct_result['abi']
        # abi = data.abi

        eth = EthReputation(contract_address=contract_address, abi=abi)

        complain_count = 0
        has_not_delay = True
        has_regulation_observance = True

        eth.issue_doctor_repute_customer_scoring(
            doctor_id,
            complain_count,
            has_not_delay,
            has_regulation_observance)

        repute = eth.issued_doctor_repute(doctor_id)

        try:
            dt = Doctor.objects.filter(ethAddress=doctor_id).order_by('-id').first()
            if dt is not None:
                dt.repute = repute
                dt.save()
        except ObjectDoesNotExist:
            pass

        try:
            rp = Reputation.objects.get(doctorId=doctor_id)
        except ObjectDoesNotExist:
            rp = Reputation()

        print(rp)
        rp.repute = repute
        rp.updateDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rp.save()
        return HttpResponseRedirect(reverse('reputation_scoring'))
