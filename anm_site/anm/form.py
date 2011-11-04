#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga

from django import forms

from models import *


class AddReportform(forms.ModelForm):

    class Meta:
        model = Report


class ModifOrgform(forms.ModelForm):

    class Meta:
        model = Organization_chart


class Memberform(forms.ModelForm):

    class Meta:
        model = Member
