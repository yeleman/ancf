#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


from models import *
from django import forms


class AddReportform(forms.ModelForm):

    class Meta:
        model = Report



