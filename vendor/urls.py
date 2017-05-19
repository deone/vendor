from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VendorAuthenticationForm
from vend import views

urlpatterns = [
    url(r'^login$', auth_views.login, {
        'template_name': 'accounts/login.html',
        'authentication_form': VendorAuthenticationForm
    }, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
]

urlpatterns += [
    url(r'^$', views.STDVendView.as_view(), name='standard_vend'),
    url(r'^vend/instant$', views.INSVendView.as_view(), name='instant_vend'),
    url(r'^my_vends$', views.get_user_vends, name='user_vends'),
    # Daily Reports
    url(r'^vends$', views.get_vends),
]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]