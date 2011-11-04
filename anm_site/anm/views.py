#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


import os

from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from anm.models import *
from form import AddReportform


def add_organization_chart(request):

    return render_to_response('add_organization_chart.html', {})


def add_rapport(request):
    """ """
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddReportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_organization_chart')
    else:
        form = AddReportform()
    c.update({'form': form})
    return render_to_response('add_rapport.html', c)


def consultation_report(request):
    """ """
    c = {}
    c.update(csrf(request))
    reports = Report.objects.all()
    for report in reports:
        report.url_report = reverse("download", args=[report.report_pdf])
    c.update({"report": reports})
    return render_to_response('consultation.html', c)

def download(request, fullpath):
    """ """
    response = HttpResponse(file(fullpath).read())
    #Si c'est un fichier pdf
    response['Content-Type'] = 'application/pdf'
    #~ response['Content-disposition'] = 'attachment'
    return response
