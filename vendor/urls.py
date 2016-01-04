from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VendorAuthenticationForm
from vend.forms import VendStandardVoucherForm, VendInstantVoucherForm
from vend import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.index,
      {
        'template': 'vend/index.html',
        'vend_form': VendStandardVoucherForm,
      },
      name='index'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html', 'authentication_form': VendorAuthenticationForm}, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]
