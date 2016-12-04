from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import VendStandardVoucherForm
from .helpers import get_price_choices

import requests
from datetime import datetime

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

def paginate(request, lst):
    paginator = Paginator(lst, settings.VENDS_PER_PAGE)
    page = request.GET.get('page')
    try:
        vends = paginator.page(page)
    except PageNotAnInteger:
        vends = paginator.page(1)
    except EmptyPage:
        vends = paginator.page(paginator.num_pages)

    return vends

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
            lst = [{
                'value': r['value'],
                'phone_number': r['phone_number'],
                'date_of_vend': datetime.strptime(r['date_of_vend'].split('.')[0], "%Y-%m-%d %H:%M:%S")} for r in response['result']]

            vends = paginate(request, lst)
            context.update({'vends': vends})
        else:
            context.update({'message': response['message']})

    return render(request, 'vend/report.html', context)