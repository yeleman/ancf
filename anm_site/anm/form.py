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
        exclude = ['date']


class Memberform(forms.ModelForm):

    class Meta:
        model = Member


class Newsletterform(forms.ModelForm):

    class Meta:
        model = Newsletter
        exclude = ['date']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur")
    password = forms.CharField(max_length=100, label="Mot de passe",\
                               widget=forms.PasswordInput)
