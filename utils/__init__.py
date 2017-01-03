from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from vend.models import Vendor, Vend

import requests

def file_generator(_file):
    with open(_file.name, 'r') as f:
        for line in f:
            yield line

def get_price_choices(voucher_type):
    lst = [('', 'Select Price')]

    prices = requests.get(settings.VOUCHER_VALUES_URL, params={'voucher_type': voucher_type}).json()
    for p in prices['results']:
        lst.append((p, str(p) + ' GHS'))

    return lst

def zeropad(num):
    num = str(num)
    return ('0' * (10 - len(num))) + num

def write_vouchers(voucher_list, _file):
    for v in voucher_list:
        with open(_file, 'a') as f:
            if len(v) == 2:
                f.write(zeropad(v[0]) + ',' + v[1] + '\r\n')
            else:
                f.write(zeropad(v[0]) + ',' + v[1] + ',' + v[2] + '\r\n')

    return f

def send_api_request(url, data):
    get_response = requests.get(url)
    post_response = requests.post(
          url,
          data=data,
          headers={"X-CSRFToken": get_response.cookies['csrftoken']},
          cookies=get_response.cookies
        )

    return post_response.json()

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

def get_active_vendors(start=None, end=None, date={}):
    # Get vendors who made vends
    if date is not None:
        distinct_vendor_ids = set([v.vendor.pk for v in Vend.objects.all() if v.occurred(**date)])
    else:
        distinct_vendor_ids = set([v.vendor.pk for v in Vend.objects.all() if v.occurred_between(start, end)])

    return [Vendor.objects.get(pk=pk) for pk in distinct_vendor_ids]

def get_vendor_vends(start=None, end=None, date={}):
    if date is not None:
        vendors = get_active_vendors(start=None, end=None, date=date)
    else:
        vendors = get_active_vendors(start=start, end=end, date=None)

    # Update each dictionary in list with vends count
    vendor_list = []
    for vendor in vendors:
        vends_list = []
        for voucher_value in settings.VOUCHER_VALUES:
            if date is not None:
                vend_count = len([v for v in Vend.objects.filter(vendor=vendor, voucher_value=voucher_value) if v.occurred(**date)])
            else:
                vend_count = len([v for v in Vend.objects.filter(vendor=vendor, voucher_value=voucher_value) if v.occurred_between(start, end)])

            vends_list.append({'value': voucher_value, 'count': vend_count})

        vendor_dict = vendor.to_dict()
        vendor_dict.update({'vend_count': vends_list})
        vendor_list.append(vendor_dict)

    return vendor_list