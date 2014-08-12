# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from ric.core.mail import events
from zope.event import notify


class SendMail(BrowserView):

    def send_mail(self):
        """
        Fire the event to send mails
        """
        filter = self.request.get('filter') or None
        if not filter:
            return

        if filter == "non_contributor":
            year = int(self.request.get('option'))
            recipients = [str(year) + '@foo.be']
            notify(events.SendNonContributor(self.context, recipients))

        elif filter == "cotisation_person":
            recipients = ['cotisation@foo.be']
            notify(events.SendCotisationPerson(self.context, recipients))

        elif filter == "organisation_members":
            organisation = self.request.get('option')
            recipients = [organisation + '@foo.be']
            notify(events.SendOrganisationMembers(self.context, recipients))

        elif filter == "non_connected_members":
            days = int(self.request.get('option'))
            recipients = [str(days) + '@foo.be']
            notify(events.SendNonConnectedMembers(self.context, recipients))

        elif filter == "send_mail_field":
            fields = self.request.get('option')
            recipients = fields
            notify(events.SendMailField(self.context, recipients))

        return 'Mails envoyés'
