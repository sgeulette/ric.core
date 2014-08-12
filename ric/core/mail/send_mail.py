# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Products.CMFCore.utils import getToolByName
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
            members = self.get_non_connected_members(days)
            recipients = [member.getProperty('email') for member in members]
            notify(events.SendNonConnectedMembers(self.context, recipients))

        elif filter == "send_mail_field":
            fields = self.request.get('option')
            recipients = fields
            notify(events.SendMailField(self.context, recipients))

        return u'Mails envoyés'

    def get_non_connected_members(self, days):
        """
        Return members not seen since days time
        """
        mt = getToolByName(self.context, 'portal_membership')
        members = mt.listMembers()

        non_connected_members = []
        for m in members:
            date_limit = datetime.now() - relativedelta(days=+days)
            last_login_time = convert_datetime(m.getProperty('last_login_time'))
            if last_login_time < date_limit:
                non_connected_members.append(m)

        return non_connected_members


def convert_datetime(plone_datetime):
    """
    Convert plone DateTime to python datetime
    """
    return datetime(year=plone_datetime.year(),
                    month=plone_datetime.month(),
                    day=plone_datetime.day(),
                    minute=plone_datetime.minute(),
                    second=int(plone_datetime.second()))
