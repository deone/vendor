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
    now = timezone.now()
    distinct_vendor_ids = set([v.vendor.pk for v in Vend.objects.filter(
        vend_date__year=now.year,
        vend_date__month=now.month,
        vend_date__day=now.day
        )])
    vendors = [Vendor.objects.get(pk=pk).to_dict() for pk in distinct_vendor_ids]
    return JsonResponse({'code': 200, 'results': vendors})

@ensure_csrf_cookie
def get_vends_count(request, vendor_id, voucher_value):
    # Return number of voucher vends by vendor
    print 'Vendor ID', vendor_id
    print 'Voucher value', voucher_value

@ensure_csrf_cookie
def get_vends_value(request, vendor_id, voucher_value):
    # Return value of voucher vends by vendor
    pass