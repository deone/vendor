from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VendorAuthenticationForm
from vend.forms import VendStandardVoucherForm, VendInstantVoucherForm
from vend import views

urlpatterns = [
    url(r'^$', views.index,
      {
        'template': 'vend/vend_standard.html',
        'vend_form': VendStandardVoucherForm,
      },
      name='vend_standard'),
    url(r'^vend/instant/$', views.index,
      {
        'template': 'vend/vend_instant.html',
        'vend_form': VendInstantVoucherForm,
      },
      name='vend_instant'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': VendorAuthenticationForm}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]
