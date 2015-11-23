from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import VendForm

@login_required
def index(request):
    context = {}
    if request.method == 'POST':
        form = VendForm(request.POST)
    else:
        form = VendForm()

    context.update({'form': form})
    return render(request, 'vend/index.html', context)
