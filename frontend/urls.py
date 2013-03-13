from django.conf.urls.defaults import *

urlpatterns=patterns('django.contrib.auth.views',
    url(r'^login/$','login'),
    url(r'^logout/$','logout'),
)

urlpatterns +=patterns('frontend.views',
    url(r'^course/$','course'),
    url(r'^user/$','user'),
    url(r'^problem/$','problem'),
    url(r'^essay/$','essay'),
    url(r'^essaygrade/$','essaygrade'),
    url(r'^membership/$','membership'),
    url(r'^userprofile/$','userprofile'),
    url(r'^organization/$','organization'),
    url(r'^register/$','register'),
    url(r'^$','index'),
)



