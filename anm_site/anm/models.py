#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import datetime
from django.db import models
from tinymce.models import HTMLField


class TypePost(models.Model):
    """ """
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    name = models.CharField(u"Nom", max_length=150)

    def __unicode__(self):
        return (u'%(name)s/%(slug)s') % {'name': self.name, 'slug': self.slug}


class Member(models.Model):
    """ """
    last_name = models.CharField(max_length=100, verbose_name=("Nom"))
    first_name = models.CharField(max_length=100, verbose_name=("Prénom"))
    image = models.ImageField(upload_to='images_member/', blank=True,
                                                verbose_name=("Photo"))
    post = models.ForeignKey(TypePost,
                                    verbose_name=("Poste occupé"))
    email = models.EmailField(max_length=75, verbose_name=("E-mail"),
                                                           unique=True)
    status = models.BooleanField(default=True, verbose_name=("Statut"))

    def __unicode__(self):
        return (u'%(last_name)s %(first_name)s') % \
                   {'last_name': self.last_name, 'first_name': self.first_name}


class Organization_chart(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),
                                               default=datetime.datetime.today)
    president = models.ForeignKey(Member, null=True, blank=True,
                                          related_name=(u"president"),
                                          verbose_name=(u"Président"))
    vice_president = models.ForeignKey(Member, null=True, blank=True,
                                              related_name=("vice_president"),
                                              verbose_name=(u"Vice Président"))
    raporter = models.ForeignKey(Member, null=True, blank=True,
                                related_name=("raporter"),
                                verbose_name=(u"Rapporteur Général"))
    assistant1 = models.ForeignKey(Member, null=True, blank=True,
                                            related_name=(u"assistant1"),
                                            verbose_name=(u"Assistant"))
    assistant2 = models.ForeignKey(Member, null=True, blank=True,
                                            related_name=(u"assistant2"),
                                            verbose_name=(u"Assistant"))
    assistant3 = models.ForeignKey(Member, null=True, blank=True,
                                            related_name=(u"assistant3"),
                                            verbose_name=(u"Assistant"))
    cordinator = models.ForeignKey(Member, null=True, blank=True,
                                         related_name=(u"cordinator"),
                                         verbose_name=(u"Coordinateur"))
    vice_cordinator = models.ForeignKey(Member, null=True, blank=True,
                                        related_name=(u"vice_cordinator"),
                                        verbose_name=(u"Vice Coordinateur"))
    fix = models.ForeignKey(Member, null=True, blank=True,
                                    related_name=(u"fix"),
                                    verbose_name=(u"Expert en fixalité"))
    gestion = models.ForeignKey(Member, null=True, blank=True,
                                    related_name=(u"gestion"),
                                    verbose_name=(u"Assistante de gestion"))
    assistant_fix = models.ForeignKey(Member, null=True, blank=True,
                                        related_name=(u"assistant_fix"),
                                        verbose_name=(u"Assistant en fixalité"))

    def __unicode__(self):
        return (u'%(president)s %(date)s') % {'president': self.president,
                                                             'date': self.date}


class TypeReport(models.Model):
    """ """
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    name = models.CharField(u"Nom", max_length=150)

    def __unicode__(self):
        return (u'%(name)s/%(slug)s') % {'name': self.name, 'slug': self.slug}


class Report(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),
                             default=datetime.datetime.today)
    title_report = models.CharField(max_length=100, verbose_name=("Titre"))
    description = models.TextField(blank=True, verbose_name=("Description"))
    report_pdf = models.FileField(upload_to='report_doc/',
                                        verbose_name=('Le rapport'), null=True)
    author = models.ForeignKey(Member, verbose_name=("Rapporteur"))
    type_report = models.ForeignKey(TypeReport,
                                              verbose_name=("Type de rapport"))

    def __unicode__(self):
        return (u'%(author)s %(type)s %(description)s %(date)s') % \
                       {'author': self.author, 'description': self.description,
                                  'type': self.title_report, 'date': self.date}


class News(models.Model):
    """ """
    title = models.CharField(max_length=100, verbose_name=("Titre"))
    comment = models.TextField(blank=True, verbose_name=("Contenu"))
    author = models.ForeignKey(Member, verbose_name=("Auteur"))
    date = models.DateField(verbose_name=("Fait le"),
                             default=datetime.datetime.today)

    def __unicode__(self):
        return (u'%(title)s %(date)s') % {'title': self.title,
                                                             'date': self.date}


class Newsletter(models.Model):
    """ """
    date = models.DateField(verbose_name=("Date d'inscription"),
                                               default=datetime.datetime.today)
    email = models.EmailField(max_length=75, verbose_name=("E-mail"),
                                                                   unique=True)

    def __unicode__(self):
        return (u'%(email)s %(date)s') % {'email': self.email,
                                                             'date': self.date}


class TextStatic(models.Model):
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    text = HTMLField(blank=True, verbose_name=("Texte"))

    def __unicode__(self):
        return (u'%(slug)s') % {'slug': self.slug}
