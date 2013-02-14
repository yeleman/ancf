#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga

from django import forms

from models import (Member, Report, Organization_chart, News, Newsletter,
                    TextStatic)


class AddReportform(forms.ModelForm):

    class Meta:
        model = Report


class AddTextStaticform(forms.ModelForm):

    class Meta:
        model = TextStatic
        exclude = ['slug']


class ModifOrgform(forms.ModelForm):

    class Meta:
        model = Organization_chart
        exclude = ['date']


class Newsform(forms.ModelForm):

    class Meta:
        model = News


class Memberform(forms.ModelForm):

    class Meta:
        model = Member
        exclude = ['status']


class Editmemberform(forms.ModelForm):

    class Meta:
        model = Member


class Newsletterform(forms.ModelForm):

    class Meta:
        model = Newsletter
        exclude = ['date']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Identifiant")
    password = forms.CharField(max_length=100, label="Mot de passe",
                               widget=forms.PasswordInput)


class UnsubscribeForm(forms.Form):
    email_unsubscribe = forms.EmailField(max_length=100,
                        label="Vérifiez l'adresse e-mail pour vous désabonner")
