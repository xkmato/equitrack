from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^pc_number$', 'equitrack.views.home', name='home'),
    url(r'^validate_number$', 'equitrack.views.validate', name='validate'),
    url(r'^acknowledge', 'equitrack.views.acknowledge', name='acknowledge'),
    # url(r'^equitrack/', include('equitrack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
