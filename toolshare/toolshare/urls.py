from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin
from search.views import search
admin.autodiscover()
# Change has been made by Dom

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^tool/', include('Tool.urls', namespace='tool')),
    url(r'^shed/', include('Shed.urls', namespace='shed')),
    url(r'^borrow/', include('borrow.urls', namespace='borrow')),
    url(r'^accounts/', include('share_user.urls', namespace='accounts')),
    url(r'^accounts/change_password_done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^messages/', include('postman.urls')),
    url(r'^terms/', TemplateView.as_view(template_name='TOC.html'), name='Terms_And_Conditions'),
    url(r'^privacy/', TemplateView.as_view(template_name='PP.html'), name='Privacy_Policy'),
    url(r'^licenses/', TemplateView.as_view(template_name='LicensesUsed.html'), name='LicensesUsed'),
    url(r'^easteregg/', TemplateView.as_view(template_name='EasterEgg.html'), name='EasterEgg'),
    url(r'^search/', search, name='search'),
)
