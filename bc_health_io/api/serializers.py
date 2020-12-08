import django
from django.contrib.auth.models import User, Group
from django.utils.datetime_safe import time
from rest_framework import serializers
from main.models import HbBlockData, Doctor, Client, Mediator, SmartContract, Reception, DeployedContract
from reputation.models import Reputation


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class HbBlockDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HbBlockData
        fields = ['ownerBlockId', 'email', 'comments', 'url', 'createDate']


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Doctor
        fields = ['ethAddress', 'email', 'repute', 'status', 'has_repute', 'createDate']


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ['ethAddress', 'email', 'createDate']


class DeployedContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeployedContract
        fields = ['contractAddress', 'contractName', 'abi', 'deployDate']

    contractAddress = serializers.CharField(max_length=42)
    contractName = serializers.CharField(max_length=1024)
    abi = serializers.CharField(max_length=4096)
    deployDate = serializers.DateTimeField(default=django.utils.timezone.now)


class DeployedReputationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeployedContract
        fields = ['contractAddress', 'contractName', 'abi', 'deployDate', 'repute']

    contractAddress = serializers.CharField(max_length=42)
    contractName = serializers.CharField(max_length=1024)
    abi = serializers.CharField(max_length=4096)
    deployDate = serializers.DateTimeField(default=django.utils.timezone.now)
    repute = serializers.IntegerField(default=0)


class ReputationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reputation
        fields = ['doctorId', 'email', 'repute', 'createDate', 'updateDate']

    doctorId = serializers.CharField(required=True, allow_blank=False, max_length=42)
    email = serializers.CharField(required=True, allow_blank=False, max_length=255)
    repute = serializers.IntegerField(read_only=False)
    createDate = serializers.DateTimeField()
    updateDate = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Reputation` instance, given the validated data.
        """
        return Reputation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Reputation` instance, given the validated data.
        """
        instance.email = validated_data.get('email', instance.email)
        instance.repute = validated_data.get('repute', instance.repute)
        instance.updateDate = validated_data.get('updateDate', instance.updateDate)
        instance.save()
        return instance


class ReceptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Reception
        fields = ['rid', 'mediatorId', 'receptionistId', 'adopterId', 'comments', 'opinions', 'status', 'url', 'hash',
                  'createDate', 'opinionDate', 'confirmDate']
        rid = serializers.CharField(required=True, allow_blank=False, max_length=42)
        mediatorId = serializers.CharField(required=True, allow_blank=False, max_length=42)
        receptionistId = serializers.CharField(required=True, allow_blank=False, max_length=42)
        adopterId = serializers.CharField(required=True, allow_blank=False, max_length=42)

        comments = serializers.CharField(allow_blank=True)
        opinions = serializers.CharField(allow_blank=True)

        status = serializers.IntegerField()
        url = serializers.CharField(allow_blank=True, max_length=1024)
        hash = serializers.CharField(allow_blank=True, max_length=256)
        createDate = serializers.DateTimeField()
        opinionDate = serializers.DateTimeField()
        confirmDate = serializers.DateTimeField()

    def create(self, validated_data):
        """
        Create and return a new `Reception` instance, given the validated data.
        """
        return Reception.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Reputation` instance, given the validated data.
        """
        instance.mediatorId = validated_data.get('mediatorId', instance.mediatorId)
        instance.receptionistId = validated_data.get('receptionistId', instance.receptionistId)
        instance.adopterId = validated_data.get('adopterId', instance.adopterId)
        instance.comments = validated_data.get('comments', instance.comments)

        instance.opinions = validated_data.get('opinions', instance.opinions)

        instance.status = validated_data.get('status', instance.status)
        instance.status = validated_data.get('opinionDate', instance.opinionDate)
        instance.status = validated_data.get('confirmDate', instance.confirmDate)

        instance.save()
        return instance


class MediatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mediator
        fields = ['mid', 'ethAddress', 'name']


class SmartContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SmartContract
        fields = ['contractAddress', 'contractDate', 'contractName', 'contractType']

