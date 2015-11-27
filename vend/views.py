from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import VendForm
from .helpers import write_vouchers

def file_generator(_file):
    with open(_file.name, 'r') as f:
        for line in f:
            yield line

@login_required
def index(request):
    context = {}
    if request.method == 'POST':
        form = VendForm(request.POST, user=request.user)
        if form.is_valid():
            response = form.save()
            vouchers = response['results']

            # Write vouchers to file and return download
            file_name = 'Voucher_' + timezone.now().strftime('%d-%m-%Y_%I:%M') + '.csv'
            _file = settings.VOUCHER_DOWNLOAD_PATH + '/' + file_name

            f = write_vouchers(vouchers, _file)

            response = HttpResponse(file_generator(f), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
            return response
    else:
        form = VendForm()

    context.update({'form': form})
    return render(request, 'vend/index.html', context)
