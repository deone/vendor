from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import VendForm
from .models import Vend, Vendor

from utils import write_vouchers, get_price_choices, paginate, get_vendor_vends

import datetime

class VendView(FormView):
    form_class = VendForm
    template_name = 'vend/vend_standard.html'
    voucher_type = 'STD'

    def get_form_kwargs(self):
        kwargs = super(VendView, self).get_form_kwargs()
        kwargs['voucher_type'] = self.voucher_type
        kwargs['prices'] = get_price_choices(self.voucher_type)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = form.save()
        messages.success(self.request, 'Vend successful.')
        return redirect('standard_vend')

class STDVendView(VendView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.request.user.vendor.voucher_type == 'INS':
            return redirect('instant_vend')
        return super(STDVendView, self).dispatch(*args, **kwargs)

class INSVendView(VendView):
    form_class = VendForm
    template_name = 'vend/vend_instant.html'
    voucher_type = 'INS'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(INSVendView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        return form.save()

@login_required
def get_user_vends(request):
    context = {
        'voucher_types': settings.VOUCHER_TYPES,
        'voucher_types_map': settings.VOUCHER_TYPES_MAP
    }

    lst = Vend.objects.filter(vendor=request.user.vendor).order_by('-vend_date')
    if not lst:
        context.update({'message': 'No vends found.'})
    else:
        vends = paginate(request, lst)
        context.update({'vends': vends})
        
    return render(request, 'vend/vends.html', context)

@ensure_csrf_cookie
def get_vendor_vend_count(request):
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

    return JsonResponse({'vendors': vendor_list, 'voucher_values': settings.VOUCHER_VALUES})