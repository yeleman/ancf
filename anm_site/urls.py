# -*- coding: utf-8 -*-

import settings

from django.conf.urls.defaults import *
from django.contrib import admin

from settings import MEDIA_ROOT, DEBUG
admin.autodiscover()


urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', "anm.views.login", name="login"),
    url(r"^logout$", "anm.views.logout", name="logout"),
    url(r'^login$', "anm.views.login", name="login"),
    url(r'^dashboard$', "anm.views.dashboard", name="dashboard"),
    url(r'^consultation_report', "anm.views.consultation_report", \
                                        name="consultation_report"),
    url(r'^help', "anm.views.help", name="help"),
    url(r'^organization_chart$', "anm.views.organization_chart", \
                                            name="organization_chart"),
    url(r'^download/(?P<path>.*)$', 'anm.views.download', name="download"),
    url(r'^add_rapport', "anm.views.add_rapport", name="add_rapport"),
    url(r'^modif_organization_chart$', "anm.views.modif_organization_chart", \
                                    name="modif_organization_chart"),

    url(r'^add_member', "anm.views.add_member", name="add_member"),
    url(r'^member', "anm.views.member", name="member"),
    url(r'^news', "anm.views.news", name="news"),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
