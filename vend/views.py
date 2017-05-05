from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .forms import VendForm
from .models import Vend, Vendor

from utils import write_vouchers, get_price_choices, paginate, get_vendor_vends

import datetime

@login_required
def index(request, template=None, prices=None, voucher_type=None):
    context = {}
    if request.method == 'POST':
        form = VendForm(request.POST, user=request.user, prices=prices, voucher_type=voucher_type)
        if form.is_valid():
            response = form.save()
            if 'code' in response:
                if response['code'] == 200:
                    messages.success(request, response['message'])
                else:
                    messages.error(request, response['message'])

                return redirect('vend:standard')

            return response
    else:
        form = VendForm(prices=prices, voucher_type=voucher_type)

    context.update({'form': form, 'voucher_types': settings.VOUCHER_TYPES})
    return render(request, template, context)

@login_required
def get_user_vends(request):
    context = {
        'voucher_types': settings.VOUCHER_TYPES,
        'voucher_types_map': settings.VOUCHER_TYPES_MAP
    }
    if request.method == 'POST':
        pass
    else:
        lst = Vend.objects.filter(vendor=request.user.vendor).order_by('-vend_date')
        if lst == []:
            context.update({'message': 'No vends found.'})
        else:
            vends = paginate(request, lst)
            context.update({'vends': vends})
        
    return render(request, 'vend/vends.html', context)

@ensure_csrf_cookie
def get_vends(request):
    # _from and to should be in the 'dd-mm-yyyy' format.
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    day = request.GET.get('day', None)
    
    _from = request.GET.get('from', None)
    to = request.GET.get('to', None)
    
    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)
    
    date = {}
    if year and month and day:
        date = {'year': year, 'month': month, 'day': day}
    elif day is None and month and year:
        date = {'year': year, 'month': month}
    elif month is None and day is None and year:
        date = {'year': year}

    if date:
        vendor_list = get_vendor_vends(start=None, end=None, date=date)
    else:
        _from = _from.split('-')
        to = to.split('-')
        
        start = datetime.date(int(_from[2]), int(_from[1]), int(_from[0]))
        end = datetime.date(int(to[2]), int(to[1]), int(to[0]))
        
        vendor_list = get_vendor_vends(start=start, end=end, date=None)

    return JsonResponse({
        'code': 200,
        'results': {'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES}
    })
