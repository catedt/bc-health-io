from django import forms
from main.models import HbBlockData, Reception


class BlockForm(forms.ModelForm):
    class Meta:
        model = HbBlockData
        fields = ['ownerBlockId', 'comments', 'url', 'publicKey', 'createDate']


class ReceptionForm(forms.ModelForm):
    class Meta:
        model = Reception
        fields = ['rid', 'mediatorId', 'receptionistId', 'adopterId', 'comments', 'opinions', 'status', 'url', 'hash',
                  'createDate', 'opinionDate', 'confirmDate']

