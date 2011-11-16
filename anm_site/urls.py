# -*- coding: utf-8 -*-

import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from settings import MEDIA_ROOT, DEBUG
admin.autodiscover()


urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', "anm.views.dashboard", name="dashboard"),
    url(r'modif_organization_chart', "anm.views.modif_organization_chart", \
                                            name="modif_organization_chart"),
    url(r'^download/(?P<path>.*)$', 'anm.views.download', \
                                                        name="download"),
    url(r'add_rapport', "anm.views.add_rapport", name="add_rapport"),
    url(r'add_member', "anm.views.add_member", name="add_member"),
    url(r'consultation_report', "anm.views.consultation_report", \
                                            name="consultation_report"),

)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
