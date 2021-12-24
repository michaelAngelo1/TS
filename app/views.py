"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views import generic
from .models import Promo, Telemarketing, Akun,Player, Deposit, Withdraw, TransferAntarAkun, Bonus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Sum

import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.forms import ReportForm

@login_required(login_url='/accounts/login')
def home(request):
    """Renders the home page."""

    akunMaster = Akun.objects.get(NamaAkun__iexact="MASTER")
    # saldo = Akun.objects.order_by('Saldo')
    
    context = {
        'akunMaster': akunMaster,    
    }

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/home.html',
        context = context
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

class DepositListView(generic.ListView):
    model = Deposit
    template_name = 'deposit_list'

# pk error
def report(request, pk):
    """Renders the report page."""

    num_deposit = Deposit.objects.all().aggregate(Sum('Nominal'))
    num_withdraw = Withdraw.objects.all().aggregate(Sum('Nominal'))

    # Deposit
    # pk diisi apa
    deposit_instance = get_object_or_404(Deposit, pk=pk)

    if request.method == 'POST':
        
        form = ReportForm(request.POST)

        if form.is_valid():
            deposit_instance.Tanggal = form.cleaned_data['input_date']
            deposit_instance.save()

            return HttpResponseRedirect(reverse('deposit-list'))


    context = {
        'num_deposit': num_deposit,
        'num_withdraw': num_withdraw,
        'form': form,
        'deposit_instance': deposit_instance,
    }

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/report.html',
        context = context
    )