from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^tasklist/', loginpage),
    url(r'^login/$', login),
    #url(r'^tasklist/(?P<id>\w+)$', index),
    url(r'^applyForm/(?P<ID>\w+)$', applyForm),
    url(r'^apply/$', applyform),
    url(r'^task/(?P<times>\w+)/(?P<ID>\w+)$', task),
    url(r'^addAnswer1/$', addAnswer1),
    url(r'^addAnswer2/$', addAnswer2),
    url(r'^addAnswer3/$', addAnswer3),
    url(r'^ajax2/$', ajax2),
    url(r'^ajax3/$', ajax3),
]