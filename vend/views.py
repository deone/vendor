from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .forms import VendForm
from .models import Vend, Vendor

from utils import write_vouchers, get_price_choices

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
    # _from = request.GET['from']
    # to = request.GET['to']

    print _from, to

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

    # Get vendors who made vends
    distinct_vendor_ids = set([v.vendor.pk for v in Vend.objects.all() if v.occurred(**date)])
    vendors = [Vendor.objects.get(pk=pk) for pk in distinct_vendor_ids]
    
    # Update each dictionary in list with vends count
    vendor_list = []
    for vendor in vendors:
        vends_list = []
        for voucher_value in settings.VOUCHER_VALUES:
            vend_count = len([v for v in Vend.objects.filter(vendor=vendor, voucher_value=voucher_value) if v.occurred(**date)])
            vends_list.append({'value': voucher_value, 'count': vend_count})

        vendor_dict = vendor.to_dict()
        vendor_dict.update({'vend_count': vends_list})
        vendor_list.append(vendor_dict)

    return JsonResponse({'code': 200, 'results': {'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES}})