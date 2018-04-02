from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.template.backends import django
from django.conf import settings
from Task.views import page_error, page_not_found
from views import *
import views2

urlpatterns = [
	url(r'^$', loginpage),
    url(r'^index/$', loginpage),
    url(r'^login/$', login),
    url(r'^applyforms/$', applyforms),
    url(r'^pwdcg/(?P<ID>\w+)$', changepassword),
    url(r'^change/$', change),
    url(r'^task1/$', task1),
    url(r'^task2/$', task2),
    url(r'^task3/$', task3),
    url(r'^inteviewlist/$', interviewlist),
    url(r'^save2/$', save2),
    url(r'^save3/$', save3),
    url(r'^marklist/$', views2.marklist)
]