#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga

from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf

from anm.models import *
from form import AddReportform

def add_organization_chart(request):

    return render_to_response('add_organization_chart.html', {})

def add_rapport(request):
    """ """
    c = {}
    c.update(csrf(request))
    report = Report()
    if request.method == 'POST':
        form = AddReportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_organization_chart')
    else:
        form = AddReportform()
    c.update({'form': form})
    return render_to_response('add_rapport.html', c)

