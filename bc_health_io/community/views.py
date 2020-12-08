from django.shortcuts import render
from community.forms import Form
from django.http import HttpResponse


def write(request):
    form = Form()
    return render(request, 'write.html', {'form': form})


def index(request):
    context = {'latest_data_list': ""}
    return render(request, 'community/index.html', context)
