from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView

from eth.eth_deploy_contract import ContractDeploy
from main.models import Reception
from main.forms import ReceptionForm

from eth.bchealtheth import BcHealthEth


bhe = BcHealthEth()

focus = {
    'main': True,
    'reputation': False,
    'community': False,
}


class ReceptionList(LoginRequiredMixin, FormView):
    login_url = 'login'
    form_class = ReceptionForm
    template_name = "main/index.html"
    success_url = "main"

    def get_context_data(self, **kwargs):
        print('{}'.format(kwargs))
        kwargs['focus'] = focus
        kwargs['latest_data_list'] = Reception.objects.all().order_by('-createDate')[:10]
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super(ReceptionList, self).form_invalid(form)
        return response

    def form_valid(self, form):
        return super(ReceptionList, self).form_valid(form)


class ReceptionDetail(LoginRequiredMixin, FormView):
    login_url = 'login'
    form_class = ReceptionForm
    template_name = "main/detail.html"
    success_url = "detail"

    def get_context_data(self, **kwargs):
        print('{}'.format(kwargs))

        kwargs['focus'] = focus
        rid = self.kwargs.get('data_id')
        data_info = Reception.objects.get(rid=rid)
        balance = bhe.get_balance(peer_address=data_info.rid)
        kwargs['block_data'] = data_info
        kwargs['balance'] = balance
        return super().get_context_data(**kwargs)

    def form_invalid(self, form):
        response = super(ReceptionDetail, self).form_invalid(form)
        return response

    def form_valid(self, form):
        return super(ReceptionDetail, self).form_valid(form)


@login_required
def mod(request, data_id):
    print('mode enter')
    if request.method == 'POST':
        form = ReceptionForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            if 'new' == data_id:
                form.save(commit=True)
            else:
                reception_info = Reception.objects.get(rid=data_id)
                if reception_info:
                    reception_info.adopterId = cleaned['adopterId']
                    reception_info.comments = cleaned['comments']
                    reception_info.opinions = cleaned['opinions']
                    reception_info.status = cleaned['status']

                    reception_info.url = cleaned['url']
                    reception_info.hash = cleaned['hash']

                    reception_info.opinionDate = cleaned['opinionDate']
                    reception_info.confirmDate = cleaned['confirmDate']

                    reception_info.email = cleaned['email']
                    reception_info.save()

            return HttpResponseRedirect(reverse('main'))
    else:
        if 'new' == data_id:
            reception_info = Reception()
        else:
            reception_info = Reception.objects.get(rid=data_id)
        form = ReceptionForm(instance=reception_info)
        context = {'block_data': reception_info, 'data_id': data_id, 'form': form}
        return render(request, 'main/write.html', context)
