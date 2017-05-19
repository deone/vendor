from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.forms import VendorAuthenticationForm

urlpatterns = [
    url(r'', include('vend.urls', namespace='vend')),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/login/$', auth_views.login, {
        'template_name': 'accounts/login.html',
        'authentication_form': VendorAuthenticationForm
    }, name='login'),
    url(r'^admin/', include(admin.site.urls)),
]