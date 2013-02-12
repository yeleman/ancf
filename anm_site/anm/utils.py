#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def html_content(data_dict):
    report = data_dict["report"]
    print "message sending ... "
    email_content = u"""<html>
                        <head>
                          <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                          <title>html title</title>
                          <style type="text/css" media="screen">
                            table{
                                background-color: #AAD373;
                                empty-cells:hide;
                            }
                            td.cell{
                                background-color: white;
                            }
                            #telechargement {
                                float: right;
                            }
                          </style>
                        </head>
                        <body style="width:740px">
                            <div class="tab-content">
                                <h4>
                                    <div id="telechargement" style='float: right;'>
                                        <a href=" %(url_report_dl)s" class = "btn">Téléchager<img src="/static/css/images/pdf.png" width="100"></a>
                                    </div>
                                    <div> <h3>Titre : %(title)s</h3></div>
                                    <div> Publié le : <small>%(date)s</small></div>
                                    <div> Rapporteur : <small>%(author)s</small></div>
                                    <fieldset ><legend>Description :</legend>
                                        <div><small> %(description)s</small></div>
                                    </fieldset>
                                </h4>
                            </div>
                            <table style="border-top: blue 1px solid;">
                                <tr><td><div style="font-family:arial,helvetica,sans-serif;font-size:12px;color:#333333"><div style="text-align:center;width:740px"><center><span>Si vous ne souhaitez plus recevoir de messages de notre part, veuillez demander votre désinscription
                                <a target="_blank" href="%(url_del_newsletter)s"> en cliquant ici</a></span><img width="1" height="1" border="0"></center>
                            </table>
                        </body>
                        </html>
                        """ % {'author': report.author, 'description': report.description,
                                'title': report.title_report, 'date': report.date, "url_report_dl": report.url_report_dl,
                                 'url_report': report.url_report}
    return email_content


def send_multipart_email(subject, data_dict, recipient_list,
                         from_email=settings.EMAIL_HOST_USER):

        subject = 'Alerte du site ANM'
        msg = EmailMultiAlternatives(subject, data_dict, from_email, recipient_list)
        msg.attach_alternative(html_content(data_dict), "text/html")
        msg.send()
