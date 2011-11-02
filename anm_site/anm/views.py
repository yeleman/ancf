#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga

from django.shortcuts import render_to_response

from anm.models import Organization_chart


def add_organization_chart(request):

    return render_to_response('add_organization_chart.html', {})
