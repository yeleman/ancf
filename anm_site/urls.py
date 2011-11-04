from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'anm_site.views.home', name='home'),
    # url(r'^anm_site/', include('anm_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'add_organization_chart', "anm.views.add_organization_chart", name="add_organization_chart"),
    url(r'^download/(?P<fullpath>.*)$', 'anm.views.download', name="download"),
    url(r'add_rapport', "anm.views.add_rapport", name="add_rapport"),
    url(r'consultation_report', "anm.views.consultation_report", name="consultation_report"),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)
