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
        return (u'%(name)s/%(slug)s') % \
        {'name': self.name, 'slug': self.slug}


class Member(models.Model):
    """ """
    last_name = models.CharField(max_length=100, verbose_name=("Nom"))
    first_name = models.CharField(max_length=100, verbose_name=("Prénom"))
    image = models.ImageField(upload_to='images_member/', blank=True,\
                                                verbose_name=("Photo"))
    post = models.ForeignKey(TypePost,
                                    verbose_name=("Poste occupé"))
    email = models.EmailField(max_length=75, verbose_name=("Email"), unique=True)
    status = models.BooleanField(default=True, verbose_name=("Status"))

    def __unicode__(self):
        return (u'%(last_name)s %(first_name)s') % \
                {'last_name': self.last_name, 'first_name': self.first_name}


class Organization_chart(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),\
                             default=datetime.datetime.today)
    president = models.ForeignKey(Member,  related_name=(u"president"), \
                                            verbose_name=(u"Président"))
    treasurer = models.ForeignKey(Member, related_name=("treasurer"), \
                                            verbose_name=(u"Trésorier"))
    assistant_Treasurer = models.ForeignKey(Member, \
                                related_name=("assistant_Treasurer"), \
                                verbose_name=(u"Adjoint trésorier"))
    secretary = models.ForeignKey(Member, related_name=(u"secretary"), \
                                            verbose_name=(u"Secrétaire"))

    def __unicode__(self):
        return (u'%(president)s %(date)s') % \
        {'president': self.president, 'date': self.date}


class TypeReport(models.Model):
    """ """
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    name = models.CharField(u"Nom", max_length=150)

    def __unicode__(self):
        return (u'%(name)s/%(slug)s') % \
        {'name': self.name, 'slug': self.slug}


class Report(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),\
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
        return (u'%(title)s %(date)s') % \
                {'title': self.title, 'date': self.date}


class Newsletter(models.Model):
    """ """
    date = models.DateField(verbose_name=("Date d'inscription"),
                             default=datetime.datetime.today)
    email = models.EmailField(max_length=75, verbose_name=("Email"), unique=True)

    def __unicode__(self):
        return (u'%(email)s %(date)s') % \
                {'email': self.email, 'date': self.date}


class TextStatic(models.Model):
    slug = models.SlugField("Code", max_length=75, primary_key=True)
    text = HTMLField(blank=True, verbose_name=("Texte"))

    def __unicode__(self):
        return (u'%(slug)s') % {'slug': self.slug}
