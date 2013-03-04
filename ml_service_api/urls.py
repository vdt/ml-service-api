from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^essay_site/', include('freeform_data.urls')),
    url(r'^frontend/', include('frontend.urls')),
)