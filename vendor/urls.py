from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VendorAuthenticationForm
from vend.forms import VendStandardVoucherForm, VendInstantVoucherForm
from vend import views
from vend.helpers import get_price_choices

urlpatterns = [
    url(r'^$', views.index,
      {
        'template': 'vend/vend_instant.html',
        'vend_form': VendInstantVoucherForm,
        'prices': get_price_choices('INS'),
      },
      name='vend_instant'),
    url(r'^vend/standard/$', views.index,
      {
        'template': 'vend/vend_standard.html',
        'vend_form': VendStandardVoucherForm,
        'prices': get_price_choices('STD'),
      },
      name='vend_standard'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': VendorAuthenticationForm}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]
