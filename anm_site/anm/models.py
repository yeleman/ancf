#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

import datetime
from django.db import models


class Member(models.Model):
    """
    """
    last_name = models.CharField(max_length=100, verbose_name=("Nom"))
    first_name = models.CharField(max_length=100, verbose_name=("Prénom"))
    image = models.ImageField(upload_to='images_member/', blank=True,\
                                                verbose_name=("Photo"))
    post = models.CharField(max_length=100, verbose_name=("Poste occupé"))
    email = models.EmailField(max_length=75, verbose_name=("Email"))
    status = models.BooleanField(default=True, verbose_name=("Status"))

    def __unicode__(self):
        return (u'%(last_name)s %(first_name)s') % \
                {'last_name': self.last_name, 'first_name': self.first_name}


class Organization_chart(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),\
                             default=datetime.datetime.today)
    president = models.ForeignKey(Member,  related_name=(u"president"), \
                                            verbose_name=(u"président"))
    treasurer = models.ForeignKey(Member, related_name=("treasurer"), \
                                            verbose_name=(u"Tresorier"))
    assistant_Treasurer = models.ForeignKey(Member, \
                                related_name=("assistant_Treasurer"), \
                                verbose_name=(u"Adjoint tresorier"))
    secretary = models.ForeignKey(Member, related_name=(u"secretary"), \
                                            verbose_name=(u"Secretaire"))

    def __unicode__(self):
        return (u'%(president)s %(date)s') % \
        {'president': self.president, 'date': self.date}


class Report(models.Model):
    """ """
    date = models.DateField(verbose_name=("Fait le"),\
                             default=datetime.datetime.today)
    type_report = models.CharField(max_length=100, verbose_name=("Titre"))
    description = models.CharField(max_length=100, \
                                            verbose_name=("description"))
    report_pdf = models.FileField(upload_to='report_doc/', \
                                  verbose_name=('Le rapport'), null=True)
    author = models.ForeignKey(Member, verbose_name=("Rapporteur"))

    def __unicode__(self):
        return (u'%(author)s %(type)s %(description)s') % \
                {'author': self.author, 'description': self.description, \
                                                'type': self.type_report}


class News(models.Model):
    """ """
    title = models.CharField(max_length=100, verbose_name=("Titre"))
    comment = models.TextField(blank=True, verbose_name=("Commentaire"))
    author = models.ForeignKey(Member, verbose_name=("Rapporteur"))
    date = models.DateField(verbose_name=("Fait le"),\
                             default=datetime.datetime.today)

    def __unicode__(self):
        return (u'%(title)s %(date)s') % \
                {'title': self.title, 'date': self.date}


class Newsletter(models.Model):
    """ """
    date = models.DateField(verbose_name=("Date d'inscription"),\
                             default=datetime.datetime.today)
    email = models.EmailField(max_length=75, verbose_name=("Email"))

    def __unicode__(self):
        return (u'%(email)s %(date)s') % \
                {'email': self.email, 'date': self.date}
