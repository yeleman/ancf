#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


from datetime import date

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import (authenticate, login as django_login,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from anm.models import Report, Organization_chart, News
from form import AddReportform, ModifOrgform, Memberform, LoginForm, \
                 Newsletterform


def login(request):
    """ page de connection """

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('administration'))
    else:
        c = {}
        c.update(csrf(request))
        state = "Se connecter"

        form = LoginForm()
        c.update({'form': form, 'state': state})

        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('add_member'))
                else:
                    state = "Your Account is not active,\
                                        please contact the site admin."
            else:
                state = u"Votre nom d'utilisateur et / ou \
                                    votre mot de passe est incorrect. \
                                    Veuillez réessayer."
            c.update({'form': form, 'state': state})
    return render_to_response('login.html', c)


def logout(request):
    """ logout est la views qui permet de se deconnecter """

    django_logout(request)
    return redirect("login")


def dashboard(request):
    """ l'accuiel"""
    c = {'category': 'dashboard'}
    c.update(csrf(request))
    try:
        statement = News.objects.latest('id')
        c.update({ "statement":statement})
    except:
        message_empty_c = "pas de comminiqué"
        c.update({"message_empty_c": message_empty_c})
    try:
        reports = Report.objects.all().order_by("-date")
        c.update({"reports":reports})
    except:
        message_empty_r = "pas de rapport"
        c.update({"message_empty_r": message_empty_r})

    if request.method == 'POST':
        form = Newsletterform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = Newsletterform()

    c.update({'form': form, })
    print c
    return render_to_response('dashboard.html', c)


@login_required
def modif_organization_chart(request):
    """ Modification du dernier organigramme """
    c = {'category': 'modif_organization_chart'}
    c.update({"user": request.user})
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


@login_required
def add_member(request):
    """ Ajout de nouveau membre """
    c = {'category': 'add_member'}
    c.update({"user": request.user})
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


