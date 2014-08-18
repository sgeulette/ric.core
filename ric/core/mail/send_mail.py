# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from plone.api.portal import show_message

from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from ric.core.mail import events
from zope.event import notify
from ric.core import RICMessageFactory as _


grok.templatedir('templates')
grok.context(Interface)


class SendMail(grok.View):
    grok.name('send_mail')
    grok.require('cmf.ManagePortal')
    grok.template('send_mail')

    def update(self):
        filter = self.request.get('filter') or None
        if not filter:
            return

        recipients = self.send_mail(filter)
        message = _(u"E-mail envoyé à")
        message = '%s: %s' % (message, ', '.join(recipients))
        show_message(message, self.request, type='info')

    def send_mail(self, filter):
        """
        Fire the event to send mails
        """
        if filter == "non_contributor":
            year = int(self.request.get('option'))
            recipients = [str(year) + '@foo.be']
            event = events.SendNonContributor(self.context, recipients)

        elif filter == "cotisation_person":
            recipients = ['cotisation@foo.be']
            event = events.SendCotisationPerson(self.context, recipients)

        elif filter == "organisation_members":
            organisation = self.request.get('option')
            recipients = [organisation + '@foo.be']
            event = events.SendOrganisationMembers(self.context, recipients)

        elif filter == "non_connected_members":
            days = int(self.request.get('option'))
            members = self.get_non_connected_members(days)
            recipients = [member.getProperty('email') for member in members]
            event = events.SendNonConnectedMembers(self.context, recipients)

        elif filter == "send_mail_field":
            fields = self.request.get('option')
            recipients = fields
            event = events.SendMailField(self.context, recipients)

        self._notify(event)
        return recipients

    @staticmethod
    def _notify(event):
        """
        Notify event
        """
        try:
            notify(event)
        except:
            raise(Exception(_(u"Un problème est survenu lors de l'envoi de l'e-mail")))

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
