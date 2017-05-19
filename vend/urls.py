from django.conf.urls import url
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.VendView.as_view(), name='standard'),
    url(r'^vend/instant$', views.VendView.as_view(voucher_type='INS', template_name='vend/vend_instant.html'), name='instant'),
]

urlpatterns += [
    url(r'^vends/$', views.get_user_vends, name='user_vends'),
]

# Daily Reports
urlpatterns += [
    url(r'^vends$', views.get_vends),
]