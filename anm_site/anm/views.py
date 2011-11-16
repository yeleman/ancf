#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


import os
from datetime import date

from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from anm.models import *
from form import AddReportform, ModifOrgform, Memberform


def dashboard(request):
    """ l'accuiel"""
    c = {'category': 'dashboard'}
    c.update(csrf(request))
    c.update({'welcome': "welcome"})
    return render_to_response('dashboard.html', c)


def modif_organization_chart(request):
    """ Modification du dernier organigramme """
    c = {'category': 'modif_organization_chart'}
    c.update(csrf(request))
    date_today = date.today()

    try:
        org_latest = Organization_chart.objects.latest('id')
        dict_org = {'president': org_latest.president, 'date': org_latest.date}
    except Organization_chart.DoesNotExist:
        dict_org = {'date': date_today}

    if request.method == 'POST':
        form = ModifOrgform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_rapport')
    else:
        form = ModifOrgform(dict_org)

    c.update({'form': form})

    return render_to_response('modif_organization_chart.html', c)


def add_rapport(request):
    """ """
    c = {'category': 'add_rapport'}
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddReportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('consultation_report')
    else:
        form = AddReportform()
    c.update({'form': form})
    return render_to_response('add_rapport.html', c)


def add_member(request):
    """ Ajout de nouveau membre """
    c = {'category': 'add_member'}
    c.update(csrf(request))
    if request.method == 'POST':
        form = Memberform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('modif_organization_chart')
    else:
        form = Memberform()
    c.update({'form': form})
    return render_to_response('add_member.html', c)


def consultation_report(request):
    """ """
    c = {'category': 'consultation'}
    c.update(csrf(request))
    reports = Report.objects.all()
    for report in reports:
        report.url_report = reverse("download", args=[report.report_pdf])
    c.update({"report": reports})
    return render_to_response('consultation.html', c)


def download(request, path):
    """ """
    fullpath = '/'.join(["media", path])
    response = HttpResponse(file(fullpath).read())
    response['Content-Type'] = 'application/pdf'
    return response
