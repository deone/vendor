from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import VendForm

from utils import write_vouchers, get_price_choices

def file_generator(_file):
    with open(_file.name, 'r') as f:
        for line in f:
            yield line

@login_required
def index(request, template=None, prices=None):
    context = {}
    if request.method == 'POST':
        form = VendForm(request.POST, user=request.user, prices=prices)
        if form.is_valid():
            response = form.save()
            return response
    else:
        form = VendForm(prices=prices)

    context.update({'form': form, 'voucher_types': settings.VOUCHER_TYPES})
    return render(request, template, context)