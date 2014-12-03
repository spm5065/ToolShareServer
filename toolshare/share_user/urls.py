__author__ = 'Noah'

from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView
from Shed.views import MyShedList
from Tool.views import MyToolList
from share_user.views import edit_profile, change_user_names, change_user_email, test_msg_send, UpdateShareUser

urlpatterns = patterns('',
        # url(r'^edit/$', TemplateView.as_view(template_name='share_user/profile_edit.html'), name='edit'),
        url(r'^change_password/$', 'django.contrib.auth.views.password_change', name='password_change'),
        url(r'^login/$', 'share_user.views.user_login', name='login'),
        url(r'^logout/$', 'share_user.views.user_logout', name='logout'),
        url(r'^register/$', 'share_user.views.user_register', name='register'),
        url(r'^profile/$', TemplateView.as_view(template_name='share_user/profile.html'), name='profile'),
        url(r'^my_sheds/$', MyShedList, name='my_shed'),
        url(r'^my_tools/$', MyToolList, name='my_tool'),
        url(r'^edit_profile/$', edit_profile, name='edit'),
        url(r'^edit_user_names/$', change_user_names, name='change_user_names'),
        url(r'^edit_user_email/$', change_user_email, name='change_user_email'),
        # url(r'^change_user_address/$', change_user_address, name='change_user_address'),
        url(r'^edit_user_address/(?P<pk>\d+)/$', UpdateShareUser.as_view(), name='change_user_address'),
        # url(r'^test/$', test_msg_send, name='test'),
)