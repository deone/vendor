from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import VendStandardVoucherForm
from .helpers import get_price_choices

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
    return render(request, 'vend/report.html', context)