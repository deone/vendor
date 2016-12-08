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

                return redirect('vend_standard')

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
def vends(request):
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
def get_vendors(request):
    # Return vendors who made vends today
    distinct_vendor_ids = set([v.vendor.pk for v in Vend.objects.all() if v.vend_date_is_today()])
    vendors = [Vendor.objects.get(pk=pk) for pk in distinct_vendor_ids]
    
    now = timezone.now()
    
    # Update each dictionary in list with vends count
    vendor_list = []
    for vendor in vendors:
        vends_list = []
        for voucher_value in settings.VOUCHER_VALUES:
            vend_count = Vend.objects.filter(vendor=vendor, voucher_value=voucher_value).filter(
                vend_date__year=now.year,
                vend_date__month=now.month,
                vend_date__day=now.day).count()
            vends_list.append({voucher_value: vend_count})

        vendor_dict = vendor.to_dict()
        vendor_dict.update({'vend_count': vends_list})
        vendor_list.append(vendor_dict)

    return JsonResponse({'code': 200, 'results': {'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES}})

@ensure_csrf_cookie
def get_vends_count(request, vendor_id, voucher_value):
    # Return number of voucher vends by vendor today
    now = timezone.now()
    vendor = Vendor.objects.get(pk=vendor_id)
    print type(vendor), type(voucher_value)
    vends_count = Vend.objects.filter(vendor=vendor, voucher_value=voucher_value).filter(
        vend_date__year=now.year,
        vend_date__month=now.month,
        vend_date__day=now.day
        ).count()
    return JsonResponse({'code': 200, 'results': vends_count})

@ensure_csrf_cookie
def get_vends_value(request, vendor_id, voucher_value):
    # Return value of voucher vends by vendor today
    vendor = Vendor.objects.get(pk=vendor_id)
    vends_value = sum([v.voucher_value for v in Vend.objects.filter(vendor=vendor, voucher_value=voucher_value) if v.vend_date_is_today()])
    return JsonResponse({'code': 200, 'results': vends_value})