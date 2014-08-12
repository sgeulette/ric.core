# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from ric.core.mail.events import SendNonContributor
from zope.event import notify


class SendMail(BrowserView):

    def send_mail(self):
        notify(SendNonContributor(self.context,
                                  self.listRecipients()))

    def listRecipients(self):
        """
        Return all recipients of the mail
        """
        # XXX add filter conditions here
        return ['test@gigi.be', 'foo@bla.be']
