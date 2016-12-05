from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import VendStandardVoucherForm, VendInstantVoucherForm
from utils import write_vouchers, get_price_choices

def file_generator(_file):
    with open(_file.name, 'r') as f:
        for line in f:
            yield line

@login_required
def index(request, template=None, vend_form=None, prices=None):
    context = {}
    if request.method == 'POST':
        form = vend_form(request.POST, user=request.user, prices=prices)
        if form.is_valid():
            response = form.save()
            vouchers = response['results']

            # Write vouchers to file and return download
            if vend_form == VendStandardVoucherForm:
                file_name = 'Vouchers_Standard_'
            elif vend_form == VendInstantVoucherForm:
                file_name = 'Vouchers_Instant_'

            file_name += timezone.now().strftime('%d-%m-%Y_%I:%M') + '.txt'
            _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name

            f = write_vouchers(vouchers, _file)

            response = HttpResponse(file_generator(f), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
            return response
    else:
        form = vend_form(prices=prices)

    context.update({'form': form})
    return render(request, template, context)
