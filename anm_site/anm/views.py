#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga

from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from anm.models import Organization_chart
from form import AddReportform

def add_organization_chart(request):

    return render_to_response('add_organization_chart.html', {})

def add_rapport(request):
    """ """
    c = {}
    c.update(csrf(request))
    form = AddReportform(request.POST)
    c.update({'form': form})
    return render_to_response('add_rapport.html', c)

