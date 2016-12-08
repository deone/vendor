from django.conf.urls import url
from django.conf import settings

from . import views
from utils import get_price_choices

urlpatterns = []

if 'STD' in settings.VOUCHER_TYPES:
    urlpatterns += [
      url(r'^$', views.index,
      {
        'template': 'vend/vend_standard.html',
        'prices': get_price_choices('STD'),
        'voucher_type': 'STD',
      },
      name='standard'),
    ]

if 'INS' in settings.VOUCHER_TYPES:
    urlpatterns += [
      url(r'^vend/instant/$', views.index,
      {
        'template': 'vend/vend_instant.html',
        'prices': get_price_choices('INS'),
        'voucher_type': 'INS',
      },
      name='instant'),
    ]

urlpatterns += [
    url(r'^vends/$', views.vends, name='vends'),
]

# Daily Reports
urlpatterns += [
    url(r'^vends/vendors/$', views.get_vendors, name='vendors'),
    url(r'^vends/count/(?P<vendor_id>\d+)/(?P<voucher_value>\d+)/$', views.get_vends_count, name='vends_count'),
    url(r'^vends/value/(?P<vendor_id>\d+)/(?P<voucher_value>\d+)/$', views.get_vends_value, name='vends_value'),
]