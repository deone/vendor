from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.VendView.as_view(), name='standard'),
    url(r'^vend/instant$', views.VendView.as_view(voucher_type='INS', template_name='vend/vend_instant.html'), name='instant'),
]

""" if 'STD' in settings.VOUCHER_TYPES:
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
    ] """

urlpatterns += [
    url(r'^vends/$', views.get_user_vends, name='user_vends'),
]

# Daily Reports
urlpatterns += [
    url(r'^vends$', views.get_vends),
]