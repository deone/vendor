from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import VendStandardVoucherForm
from .helpers import get_price_choices

import requests

@login_required
def index(request, template=None, vend_form=None, prices=None):
    context = {}
    if request.method == 'POST':
        form = vend_form(request.POST, user=request.user, prices=prices)
        if form.is_valid():
            response = form.save()
            if response['recharged'] == True:
                messages.success(request, response['message'])
                return redirect('vend_standard')
            else:
                messages.error(request, response['message'])
                return redirect('vend_standard')
    else:
        form = vend_form(prices=prices)

    context.update({'form': form})
    return render(request, template, context)

@login_required
def report(request):
    context = {}
    vendor_id = request.user.vendor.id
    if request.method == 'POST':
        pass
    else:
        response = requests.get(settings.VEND_FETCH_URL + str(vendor_id) + '/')
        response = response.json()
        if response['code'] == 200:
            context.update({'vends': response['result']})
        else:
            pass

    return render(request, 'vend/report.html', context)