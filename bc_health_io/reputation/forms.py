from django import forms
from reputation.models import Reputation


class ReputationForm(forms.ModelForm):
    class Meta:
        model = Reputation
        fields = ['doctorId', 'email', 'repute', 'createDate', 'updateDate']
