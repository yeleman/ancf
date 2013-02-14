#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fadiga

from django.core.mail import EmailMultiAlternatives

from django.conf import settings


def send_multipart_email(subject, message_html, text_content, recipient_list,
                         from_email=settings.EMAIL_HOST_USER):

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(message_html, "text/html")
        msg.send()
