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
    url(r'^vends/$', views.get_user_vends, name='user_vends'),
]

# Daily Reports
urlpatterns += [
    # url(r'^vends/vendors$', views.get_vends, name='vends'),
    url(r'^vends/(?P<year>[0-9]{4})$', views.get_vends),
    url(r'^vends/(?P<year>[0-9]{4})/(?P<month>[0-9]+)$', views.get_vends),
    url(r'^vends/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/(?P<day>[0-9]+)$', views.get_vends),
    url(r'^vends/(?P<_from>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<to>[0-9]{4}-[0-9]{2}-[0-9]{2})$', views.get_vends_by_date_range),
]