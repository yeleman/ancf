#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


from datetime import date

from django.contrib import messages
from django.shortcuts import (render_to_response, redirect,
                                                    HttpResponseRedirect)
from django.core.context_processors import csrf
from django.contrib.auth import (authenticate, login as django_login,
                                                logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.mail import send_mail


from anm.models import (Report, Organization_chart, News, Member, Newsletter,
                        TypeReport, TextStatic)
from form import (AddReportform, ModifOrgform, Memberform, LoginForm,
                                Newsletterform, Newsform, Editmemberform)


def login(request):
    """ Page de connection """

    form = LoginForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('add_member'))
    else:
        c = {}
        c.update(csrf(request))
        state = "Se connecter"

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
    return redirect("dashboard")


def dashboard(request):
    """ l'accueil """
    c = {'category': 'dashboard'}
    c.update(csrf(request))
    try:
        last_new = News.objects.latest('id')
        c.update({"last_new": last_new})
    except:
        c.update({"message_empty_c": "Pas de comminiqué"})

    reports = Report.objects.all().order_by('-date')[:3]
    try:
        textstatic = TextStatic.objects.get(slug='dashboard')
    except:
        textstatic = None
    for report in reports:
        report.url_report_date = reverse("report", args=[report.id])
    message_empty_r = "Pas de rapport"
    c.update({"reports": reports, "message_empty_r": message_empty_r,
              "textstatic": textstatic})

    if request.method == 'POST':
        form = Newsletterform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, u"Votre email a été bien enregistre")
            return redirect('dashboard')
    else:
        form = Newsletterform()

    c.update({'form': form})

    return render_to_response('dashboard.html', c)


@login_required
def add_report(request):
    """ Ajout de nouveau rapport """
    c = {'category': 'add_report'}
    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddReportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, u"Le rapport a été bien enregistre")
            try:
                recipients = [user.email for user in Newsletter.objects.all()]
            except:
                recipients = []
            print "message sending ... "
            message = u"Un nouveau rapport a été publié sur sur le " \
                      + u"http://www.yeleman.com"
            try:
                send_mail(u"Commission des Finances de l'Assemblée Nationale",
                          message, "Commission des Finances de l'Assemblée Nationale",
                          recipients, fail_silently=False)
                print "success"
            except Exception as e:
                print(e)

            return redirect('report')
    else:
        form = AddReportform()
    c.update({'form': form})
    return render_to_response('add_report.html', c)


def report(request, *args, **kwargs):
    """ Liste des rapports """
    report_id = kwargs["report_id"] or 0
    type_slug = kwargs["type_slug"] or ""

    c = {'category': 'report', "message_empty_r": "Pas de rapport"}
    c.update(csrf(request))
    try:
        selected_report = Report.objects.latest('date')
    except:
        return render_to_response('report.html', c)

    type_reports = TypeReport.objects.all()

    for type_report in type_reports:
        type_report.url_type_report = reverse("report", args=[report_id, type_report.slug])
    c.update({'type_reports': type_reports})

    if type_slug != "":
        reports = Report.objects.filter(type_report__slug=type_slug).order_by("-date")
        try:
            selected_type = TypeReport.objects.get(slug=type_slug)
            selected_report = reports[0]
            c.update({"selected_type": selected_type})
        except:
            pass
    else:
        reports = Report.objects.all().order_by("-date")
        selected_report = reports[0]

    if report_id != 0:
        try:
            selected_report = Report.objects.get(id=report_id)
        except:
            pass
    selected_report.url_report = reverse("download",
                                         args=[selected_report.report_pdf])
    for report in reports:
        report.url_report_date = reverse("report", args=[report.id, type_slug])

    c.update({"selected_report": selected_report, "reports": reports})

    return render_to_response('report.html', c)


def download(request, path):
    """ Telecharger un rapport """
    fullpath = '/'.join(["media", path])
    response = HttpResponse(file(fullpath).read())
    response['Content-Type'] = 'application/pdf'
    return response


def help(request):
    """ Page d'aide """
    c = {'category': 'aide'}
    c.update(csrf(request))
    return render_to_response("help.html", c)


def organization_chart(request):
    """ Affiche l'organigramme """
    c = {'category': 'organization_chart'}
    c.update(csrf(request))
    try:
        organization_chart = Organization_chart.objects.latest('id')
        c.update({"org": organization_chart})
    except:
        c.update({"message_empty_org": "Pas de organigramme"})
    return render_to_response("organization_chart.html", c)


@login_required
def modif_organization_chart(request):
    """ Modification du dernier organigramme """
    c = {'category': 'modif_organization_chart'}
    c.update({"user": request.user})
    c.update(csrf(request))
    date_today = date.today()

    try:
        org_latest = Organization_chart.objects.latest('id')
        dict_org = {'president': org_latest.president, \
                    'assistant_Treasurer': org_latest.assistant_Treasurer, \
                    'treasurer': org_latest.treasurer, \
                    'secretary': org_latest.secretary, \
                    'date': org_latest.date}
    except Organization_chart.DoesNotExist:
        dict_org = {'date': date_today}

    if request.method == 'POST':
        form = ModifOrgform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, u"L'organigramme à été mise à jour")
            return redirect('organization_chart')
    else:
        form = ModifOrgform(dict_org)

    c.update({'form': form})

    return render_to_response('modif_organization_chart.html', c)


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
            news_letter = Newsletter()
            news_letter.email = request.POST.get('email')
            news_letter.save()
            messages.info(request, u"le nouveau membre à été ajouter")
            return redirect('member')
    else:
        form = Memberform()
    c.update({'form': form})
    return render_to_response('add_member.html', c)


@login_required
def member(request):
    """ Liste des membres """

    c = {'category': 'member'}
    c.update(csrf(request))
    c.update({"user": request.user})
    members = Member.objects.all()
    for member in members:
        member.url_member = reverse("edit_member", args=[member.id])
    c.update({"members": members, "message_empty_m": "Pas de membre"})
    return render_to_response("member.html", c)


@login_required
def edit_member(request, *args, **kwargs):
    """ Modification de membre """

    c = {'category': 'edit_member'}
    c.update(csrf(request))
    c.update({"user": request.user})
    messages.add_message(request, messages.INFO, 'Hello world.')
    member_id = kwargs["id"]
    selected_member = Member.objects.get(id=member_id)
    dict_member = {"last_name": selected_member.last_name, \
                    "first_name": selected_member.first_name,\
                    "image": selected_member.image, \
                    "post": selected_member.post, \
                    "email": selected_member.email,\
                    "status": selected_member.status,\
                }
    if request.method == 'POST':
        form = Editmemberform(request.POST, request.FILES)
        if form.is_valid():
            selected_member.last_name = request.POST.get('last_name')
            selected_member.first_name = request.POST.get('first_name')
            if not request.FILES.get('image') == None:
                selected_member.image = request.FILES.get('image')
            selected_member.post = request.POST.get('post')
            selected_member.email = request.POST.get('email')
            if request.POST.get('status'):
                selected_member.status = request.POST.get('status')
            else:
                selected_member.status = False
            selected_member.save()
            messages.info(request, u"les informations ont été ajouter")
            return redirect('member')
    else:
        form = Editmemberform(dict_member)
    c.update({'form': form, 'image': selected_member.image})
    return render_to_response("edit_member.html", c)


@login_required
def news(request):
    """ Ajout d'avis de reunion """
    c = {'category': 'news'}
    c.update(csrf(request))
    c.update({"user": request.user})

    if request.method == 'POST':
        form = Newsform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = Newsform()
    c.update({'form': form})
    return render_to_response("news.html", c)


def history_news(request):
    """ Affiche l'historique des avis de reunion """
    c = {'category': 'history_news'}
    news = News.objects.all()
    c.update({'news': news})
    return render_to_response("history_news.html", c)


@login_required
def newsletter(request):
    """ Liste des newsletter """
    c = {'category': 'newsletter'}
    c.update(csrf(request))
    c.update({"user": request.user})

    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:
        newsletter.url_newsletter = reverse("del_newsletter", \
                                                    args=[newsletter.id])
    c.update({"newsletters": newsletters, \
                                    "message_empty_n": "Pas d'inscrit"})

    return render_to_response("news_letter.html", c)


@login_required
def del_newsletter(request, *args, **kwargs):
    """ Suppression de newsletter"""

    c = {'category': 'edit_member'}
    c.update(csrf(request))
    c.update({"user": request.user})
    id_ = kwargs["id"]
    selected = Newsletter.objects.get(id=id_)
    selected.delete()
    return redirect('newsletter')
