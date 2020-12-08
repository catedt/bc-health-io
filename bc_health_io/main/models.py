import django
from django.db import models


class DeployedContract(models.Model):
    contractAddress = models.CharField(max_length=42)
    contractName = models.CharField(max_length=1024)
    abi = models.TextField()
    deployDate = models.DateTimeField('date deployed', default=django.utils.timezone.now)
    repute = models.IntegerField(default=0)


class DeployedContractHistory(models.Model):
    contractAddress = models.CharField(max_length=42)
    contractName = models.CharField(max_length=1024)
    abi = models.TextField()
    deployDate = models.DateTimeField('date deployed', default=django.utils.timezone.now)
    repute = models.IntegerField(default=0)


class HbBlockData(models.Model):
    ownerBlockId = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, blank=False, default='unknown')

    comments = models.TextField()
    url = models.URLField(max_length=1024)

    publicKey = models.CharField(max_length=256)

    createDate = models.DateTimeField('date published', default=django.utils.timezone.now)

    def __str__(self):
        return self.ownerBlockId


class Client(models.Model):
    ethAddress = models.CharField(max_length=42)
    email = models.EmailField(max_length=70, blank=False, default='unknown')
    createDate = models.DateTimeField('Client Created', default=django.utils.timezone.now)


class Doctor(models.Model):
    ethAddress = models.CharField(max_length=42)
    email = models.EmailField(max_length=70, blank=False, default='unknown')
    repute = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    has_repute = models.BooleanField(default=False)
    createDate = models.DateTimeField('Doctor Created', default=django.utils.timezone.now)


class Mediator(models.Model):
    mid = models.IntegerField()
    ethAddress = models.CharField(max_length=42)
    name = models.CharField(max_length=256)


class Reception(models.Model):
    rid = models.CharField(max_length=42)
    mediatorId = models.IntegerField()
    receptionistId = models.CharField(max_length=42)
    adopterId = models.CharField(max_length=42)
    comments = models.TextField()
    opinions = models.TextField()
    status = models.IntegerField(default=0)

    url = models.URLField(max_length=1024)
    hash = models.CharField(max_length=256)

    createDate = models.DateTimeField('Reception Create Date', default=django.utils.timezone.now)
    opinionDate = models.DateTimeField('Opinion Date', default=None)
    confirmDate = models.DateTimeField('Confirm Date', default=None)

    class Meta:
        ordering = ['createDate']


class Opinion(models.Model):
    oid = models.IntegerField()
    receptionId = models.CharField(max_length=42)
    opinions = models.TextField()
    opinionDate = models.DateTimeField('Opinion Date', default=django.utils.timezone.now)


class SmartContract(models.Model):
    contractAddress = models.CharField(max_length=42)
    contractDate = models.DateTimeField("SmartContract Created", default=django.utils.timezone.now)
    contractName = models.CharField(max_length=256)
    contractType = models.IntegerField(default=0)