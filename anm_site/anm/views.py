#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Alou & Fadiga


from django.contrib import messages
from django.shortcuts import (render_to_response,  redirect, render,
                                                    HttpResponseRedirect)
from django.core.context_processors import csrf
from django.contrib.auth import (authenticate, login as django_login,
                                                logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from anm.models import (Report, Organization_chart, News, Member, Newsletter,
                        TypeReport, TextStatic, TypePost)
from anm.utils import send_multipart_email
from form import (AddReportform, ModifOrgform, Memberform, LoginForm,
                  Newsletterform, Newsform, Editmemberform, UnsubscribeForm,
                  AddTextStaticform)


def login(request):
    """ Page de connection """

    form = LoginForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('edit_text_static'))
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
                    return HttpResponseRedirect(reverse('edit_text_static'))
                else:
                    state = "Your Account is not active,\
                                        please contact the site admin."
            else:
                state = u"Votre nom d'utilisateur et / ou \
                                    votre mot de passe est incorrect. \
                                    Veuillez réessayer."

        c.update({'form': form, 'state': state})
    return render(request, 'login.html', c)


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

    president = Member.objects.get(post__slug="president")
    president.url_display = reverse("display_member", args=[president.id])

    reports = Report.objects.all().order_by('-date')[:3]
    try:
        textstatic = TextStatic.objects.get(slug='dashboard')
    except:
        textstatic = None

    for report in reports:
        report.url_report_date = reverse("report", args=[report.id])
    message_empty_r = "Pas de rapport"
    c.update({"reports": reports, "message_empty_r": message_empty_r,
              "textstatic": textstatic, "president": president})

    if request.method == 'POST':
        form = Newsletterform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u"Votre email a été bien enregistre")
            messages.set_level(request, messages.WARNING)
            return redirect('dashboard')
    else:
        form = Newsletterform()

    c.update({'form': form})

    return render(request, 'dashboard.html', c)


@login_required
def add_report(request):
    """ Ajout de nouveau rapport """
    c = {'category': 'add_report', 'menu': 'admin'}
    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddReportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, u"Le rapport a été mis en ligne")
            try:
                recipient_list = [user.email for user in
                                                      Newsletter.objects.all()]
            except:
                recipient_list = []
            report = Report.objects.latest('id')
            name_site = Site.objects.get_current().name
            report.url_report_dl = reverse("download",
                                                      args=[report.report_pdf])
            report.url_report = reverse("report", args=[report.id,
                                                      report.type_report.slug])

            data_dict = {"report": report,
                         "unsubscribe_url":  reverse("unsubscribe"),
                         "site_url": name_site}

            try:
                print "send email ...."
                subject = u"Un nouveau rapport a été publié sur sur le site \
                                                                %s" % name_site
                text_content = subject
                message_html = render_to_string("message_new_report.html",
                                                                     data_dict)
                send_multipart_email(subject, message_html, text_content,
                                                                recipient_list)
                print "success"
            except Exception as e:
                raise
                print(e)

            return redirect('add_report')
    else:
        form = AddReportform()
    reports = Report.objects.order_by('-date')
    for report in reports:
        report.url_del = reverse("del_report", args=[report.id])

    c.update({'form': form, 'reports': reports})
    return render(request, 'add_report.html', c)


def report(request, *args, **kwargs):
    """ Liste des rapports """
    report_id = kwargs["report_id"] or 0
    type_slug = kwargs["type_slug"] or ""

    c = {'category': 'report', "message_empty_r": "Pas de rapport"}
    c.update(csrf(request))

    type_reports = TypeReport.objects.all()

    for type_report in type_reports:
        type_report.url_type_report = reverse("report", args=[report_id,
                                                             type_report.slug])
    c.update({'type_reports': type_reports})

    try:
        selected_report = Report.objects.latest('date')
    except:
        return render(request, 'report.html', c)

    if type_slug != "":
        reports = Report.objects.filter(type_report__slug=type_slug) \
                                                             .order_by("-date")
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

    return render(request, 'report.html', c)


@login_required
def del_report(request, *args, **kwargs):
    """ Suppression de rapport"""

    c = {'category': 'del_report', 'menu': 'admin'}
    c.update(csrf(request))
    c.update({"user": request.user})
    id_ = kwargs["id"]
    selected = Report.objects.get(id=id_)
    selected.delete()
    messages.success(request, u"Le rapport a été supprimé")
    return redirect('add_report')


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
    return render(request, "help.html", c)


def organization_chart(request):
    """ Affiche l'organigramme """
    c = {'category': 'organization_chart'}
    try:
        type_member = TypePost.objects.get(slug='membre')
    except:
        type_member = None
    members = Member.objects.filter(post=type_member, status=True)
    for member in members:
        member.url_display = reverse("display_member", args=[member.id])
    try:
        organization_chart = Organization_chart.objects.latest('id')
        if organization_chart.president:
            organization_chart.president.url_display = reverse("display_member",
                                        args=[organization_chart.president.id])
        if organization_chart.vice_president:
            organization_chart.vice_president.url_display = \
                                    reverse("display_member",
                                    args=[organization_chart.vice_president.id])
        if organization_chart.raporter:
            organization_chart.raporter.url_display = reverse("display_member",
                                        args=[organization_chart.raporter.id])
        if organization_chart.assistant1:
            organization_chart.assistant1.url_display = \
                                        reverse("display_member",
                                        args=[organization_chart.assistant1.id])
        if organization_chart.assistant2:
            organization_chart.assistant2.url_display = \
                                        reverse("display_member",
                                        args=[organization_chart.assistant2.id])
        if organization_chart.assistant3:
            organization_chart.assistant3.url_display = \
                                        reverse("display_member",
                                        args=[organization_chart.assistant3.id])
        if organization_chart.cordinator:
            organization_chart.cordinator.url_display = \
                                        reverse("display_member",
                                        args=[organization_chart.cordinator.id])
        if organization_chart.vice_cordinator:
            organization_chart.vice_cordinator.url_display = \
                                reverse("display_member",
                                args=[organization_chart.vice_cordinator.id])
        if organization_chart.fix:
            organization_chart.fix.url_display = reverse("display_member",
                                        args=[organization_chart.fix.id])
        if organization_chart.gestion:
            organization_chart.gestion.url_display = reverse("display_member",
                                        args=[organization_chart.gestion.id])
        if organization_chart.assistant_fix:
            organization_chart.assistant_fix.url_display = \
                                    reverse("display_member",
                                    args=[organization_chart.assistant_fix.id])
        c.update({"org": organization_chart, 'members': members})
    except:
        raise
        pass

    c.update({"message_empty_org": "Pas de organigramme"})
    return render(request, "organization_chart.html", c)


@login_required
def modif_organization_chart(request):
    """ Modification du dernier organigramme """
    c = {'category': 'modif_organization_chart', 'menu': 'admin'}
    c.update({"user": request.user})
    c.update(csrf(request))

    try:
        org_latest = Organization_chart.objects.latest('id')
    except Organization_chart.DoesNotExist:
        org_latest = None

    if request.method == 'POST':
        form = ModifOrgform(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, u"L'organigramme a été mise à jour")
            return redirect('organization_chart')
    else:
        form = ModifOrgform(instance=org_latest)

    members = Member.objects.all()
    for member in members:
        member.url_member = reverse("edit_member", args=[member.id])

    c.update({'form': form, 'members': members})

    return render(request, 'modif_organization_chart.html', c)


@login_required
def add_member(request):
    """ Ajout de nouveau membre """
    c = {'category': 'add_member', 'menu': 'admin'}
    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = Memberform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.POST.get('email'):
                news_letter = Newsletter()
                news_letter.email = request.POST.get('email')
                news_letter.save()
            messages.success(request, u"le nouveau membre a été ajouter")
            return redirect('modif_organization_chart')
    else:
        form = Memberform()
    c.update({'form': form})
    return render(request, 'add_member.html', c)


def display_member(request, *args, **kwargs):
    c = {'category': 'display_member'}
    member_id = kwargs["id"]
    member = Member.objects.get(id=member_id)
    c.update({'member': member})
    return render(request, "display_member.html", c)


@login_required
def edit_member(request, *args, **kwargs):
    """ Modification de membre """

    c = {'category': 'edit_member', 'menu': 'admin'}
    c.update(csrf(request))
    c.update({"user": request.user})
    member_id = kwargs["id"]
    selected_member = Member.objects.get(id=member_id)
    if request.method == 'POST':
        form = Editmemberform(request.POST, request.FILES,
                                                      instance=selected_member)
        if form.is_valid():
            selected_member.last_name = request.POST.get('last_name')
            selected_member.first_name = request.POST.get('first_name')
            if request.FILES.get('image'):
                selected_member.image = request.FILES.get('image')
            post = TypePost.objects.get(slug=request.POST.get('post'))
            selected_member.post = post
            selected_member.email = request.POST.get('email')
            if request.POST.get('status'):
                selected_member.status = request.POST.get('status')
            else:
                selected_member.status = False
            selected_member.save()
            messages.success(request, u"les informations ont été mise jour")
            return redirect('modif_organization_chart')
    else:
        form = Editmemberform(instance=selected_member)
    c.update({'form': form, 'image': selected_member.image})
    return render(request, "edit_member.html", c)


@login_required
def news(request):
    """ Ajout d'avis de reunion """
    c = {'category': 'news', 'menu': 'admin'}
    c.update(csrf(request))
    c.update({"user": request.user})

    if request.method == 'POST':
        form = Newsform(request.POST)
        if form.is_valid():
            form.save()

            name_site = Site.objects.get_current().name
            try:
                recipient_list = [user.email for user in Member.objects.all()]
            except:
                recipient_list = []
            data_dict = {"new": News.objects.latest('date'),
                         "site_url": name_site}

            try:
                print "send email ...."
                subject = u"Une nouvelle brève a été publié sur sur le site " + \
                          u"%s" % name_site
                text_content = subject
                message_html = render_to_string("message_news.html", data_dict)
                send_multipart_email(subject, message_html, text_content,
                                                                recipient_list)
                print "success"
            except Exception as e:
                print(e)
                raise
            messages.success(request, u"l'informations a été publié")
            return redirect('news')
    else:
        form = Newsform()
    news = News.objects.order_by('-date')
    c.update({'form': form, 'news': news})
    return render(request, "news.html", c)


def history_news(request):
    """ Affiche l'historique des avis de reunion """
    c = {'category': 'history_news'}
    news = News.objects.all()
    c.update({'news': news})
    return render(request, "history_news.html", c)


@login_required
def newsletter(request):
    """ Liste des newsletter """
    c = {'category': 'newsletter', 'menu': 'admin'}
    c.update(csrf(request))
    c.update({"user": request.user})

    newsletters = Newsletter.objects.all()
    for newsletter in newsletters:
        newsletter.url_newsletter = reverse("del_newsletter",
                                                          args=[newsletter.id])
    c.update({"newsletters": newsletters,
                                    "message_empty_n": "Pas d'inscrit"})

    return render(request, "news_letter.html", c)


@login_required
def del_newsletter(request, *args, **kwargs):
    """ Suppression de newsletter"""

    c = {'category': 'del_newsletter', 'menu': 'admin'}
    c.update(csrf(request))
    c.update({"user": request.user})
    id_ = kwargs["id"]
    selected = Newsletter.objects.get(id=id_)
    selected.delete()
    return redirect('newsletter')


@login_required
def edit_text_static(request, *args, **kwargs):
    """ Ajout de nouveau texte de bienvenu """
    c = {'category': 'edit_text_static', 'menu': 'admin'}

    textstatic = TextStatic.objects.get(slug='dashboard')
    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddTextStaticform(request.POST, instance=textstatic)
        if form.is_valid():
            form.save()
            messages.success(request,
                            u"Le nouveau texte de présentation a été publié.")
            return redirect('dashboard')
    else:
        form = AddTextStaticform(instance=textstatic)
    c.update({'form': form})
    return render(request, 'edit_text_static.html', c)


def display_text_unacem(request):
    """ Affichage du texte de présentation de l'UNACEM """
    c = {'category': 'display_text_unacem'}

    try:
        textstatic = TextStatic.objects.get(slug='unacem')
    except:
        textstatic = None

    cordinator = Member.objects.get(post__slug="coordinataire")
    cordinator.url_display = reverse("display_member", args=[cordinator.id])
    c.update({'textstatic': textstatic, 'cordinator': cordinator})
    return render(request, 'display_text_unacem.html', c)


@login_required
def edit_text_unacem(request, *args, **kwargs):
    """ Ajout de nouveau texte de bienvenu """
    c = {'category': 'edit_text_uncef', 'menu': 'admin'}

    textstatic = TextStatic.objects.get(slug='unacem')
    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = AddTextStaticform(request.POST, instance=textstatic)
        if form.is_valid():
            form.save()
            messages.success(request,
                             u"Le nouveau texte de présentation a été publié.")
            return redirect('display_text_unacem')
    else:
        form = AddTextStaticform(instance=textstatic)
    c.update({'form': form})
    return render(request, 'edit_text_unacem.html', c)


def unsubscribe(request):
    """  """
    c = {'category': 'unsubscribe'}

    c.update({"user": request.user})
    c.update(csrf(request))
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email_unsubscribe')
            try:
                selected = Newsletter.objects.get(email=email)
            except:
                messages.warning(request, u"vous n'avez jamais été sur la liste"
                                u" de diffusion. Si vous ne souhaitez plus "
                                u"recevoir ces courriels, assurez-vous de "
                                u"dire à votre ami de cesser de les "
                                u"transmettre à vous.")
            try:
                selected.delete()
                messages.warning(request, u"Bye bye")
                return redirect('dashboard')
            except:
                pass
    else:
        form = UnsubscribeForm()
    c.update({'form': form})
    return render(request, 'unsubscribe.html', c)
