# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', "anm.views.dashboard", name="dashboard"),
    url(r"^logout$", "anm.views.logout", name="logout"),
    url(r'^login$', "anm.views.login", name="login"),
    url(r'^history_news$', "anm.views.history_news", name="history_news"),
    url(r'^help$', "anm.views.help", name="help"),
    url(r'^organization_chart$', "anm.views.organization_chart",
                                            name="organization_chart"),
    url(r'^download/(?P<path>.*)$', 'anm.views.download', name="download"),
    url(r'^add_report$', "anm.views.add_report", name="add_report"),
    url(r'^del_report/(?P<id>\d+)$', "anm.views.del_report",
                                                name="del_report"),
    url(r'^modif_organization_chart$', "anm.views.modif_organization_chart",
                                            name="modif_organization_chart"),

    url(r'^add_member$', "anm.views.add_member", name="add_member"),
    url(r'^edit_member/(?P<id>\d+)$', "anm.views.edit_member",
                                                        name="edit_member"),
    url(r'^edit_text_static$', "anm.views.edit_text_static",
                                                    name="edit_text_static"),
    url(r'^member$', "anm.views.member", name="member"),
    url(r'^report/(?:(?P<report_id>\d+)/(?P<type_slug>[a-z0-9\-]+)*)*$',
                                         "anm.views.report", name="report"),
    url(r'^news$', "anm.views.news", name="news"),
    url(r'^newsletter$', "anm.views.newsletter", name="newsletter"),
    url(r'^del_newsletter/(?P<id>\d+)$', "anm.views.del_newsletter",
                                                name="del_newsletter"),

)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
)
