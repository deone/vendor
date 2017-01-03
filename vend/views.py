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
        lst = Vend.objects.filter(vendor=request.user.vendor)
        if lst == []:
            context.update({'message': 'No vends found.'})
        else:
            vends = paginate(request, lst)
            context.update({'vends': vends})
        
    return render(request, 'vend/vends.html', context)

@ensure_csrf_cookie
def get_vends_by_date_range(request, _from, to):
    _from = _from.split('-')
    to = to.split('-')

    start = datetime.date(int(_from[0]), int(_from[1]), int(_from[2]))
    end = datetime.date(int(to[0]), int(to[1]), int(to[2]))

    vendor_list = get_vendor_vends(start=start, end=end, date=None)

    return JsonResponse({'code': 200, 'results': {'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES}})

@ensure_csrf_cookie
def get_vends(request, year=None, month=None, day=None):
    now = timezone.now()

    if year:
        year = int(year)
    if month:
        month = int(month)
    if day:
        day = int(day)

    # URL contains only year
    if month is None and day is None and year:
        if year > now.year:
            return JsonResponse({'code': 500, 'message': 'Invalid year.'})
        else:
            date = {'year': year}

    # URL contains year and month
    elif day is None and month and year:
        if year > now.year or month > now.month:
            return JsonResponse({'code': 500, 'message': 'Invalid year or month.'})
        else:
            date = {'year': year, 'month': month}

    # URL contains year, month and day
    elif year and month and day:
        date_supplied = datetime.date(year, month, day)
        if date_supplied > now.date():
            return JsonResponse({'code': 500, 'message': 'Invalid date.'})
        else:
            date = {'year': year, 'month': month, 'day': day}

    vendor_list = get_vendor_vends(start=None, end=None, date=date)

    return JsonResponse({'code': 200, 'results': {'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES}})