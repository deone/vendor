from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings

from accounts.forms import VendorAuthenticationForm
from vend.forms import VendForm
from vend import views
from utils import get_price_choices

urlpatterns = []

if 'STD' in settings.VOUCHER_TYPES:
    urlpatterns += [
      url(r'^$', views.index,
      {
        'template': 'vend/vend_standard.html',
        'prices': get_price_choices('STD'),
      },
      name='vend_standard'),
    ]

if 'INS' in settings.VOUCHER_TYPES:
    urlpatterns += [
      url(r'^vend/instant/$', views.index,
      {
        'template': 'vend/vend_instant.html',
        'prices': get_price_choices('INS'),
      },
      name='vend_instant'),
    ]

urlpatterns += [
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': VendorAuthenticationForm}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]