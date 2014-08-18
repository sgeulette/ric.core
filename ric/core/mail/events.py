# -*- coding: utf-8 -*-
from five import grok
from zope.component.interfaces import ObjectEvent

from plone.app.contentrules import handlers

from ric.core.mail import interfaces


class SendBase(ObjectEvent):

    def __init__(self, context, recipients):
        ObjectEvent.__init__(self, context)
        self.context = context
        self.context.recipients = recipients


class SendNonContributor(SendBase):
    grok.implements(interfaces.ISendNonContributor)


@grok.subscribe(interfaces.ISendNonContributor)
def send_non_contributor_subscriber(event):
    handlers.execute(event.object, event)


class SendCotisationPerson(SendBase):
    grok.implements(interfaces.ISendCotisationPerson)


@grok.subscribe(interfaces.ISendCotisationPerson)
def send_cotisation_person_subscriber(event):
    handlers.execute(event.object, event)


class SendOrganisationMembers(SendBase):
    grok.implements(interfaces.ISendOrganisationMembers)


@grok.subscribe(interfaces.ISendOrganisationMembers)
def send_organisation_members_subscriber(event):
    handlers.execute(event.object, event)


class SendNonConnectedMembers(SendBase):
    grok.implements(interfaces.ISendNonConnectedMembers)


@grok.subscribe(interfaces.ISendNonConnectedMembers)
def send_non_connected_members_subscriber(event):
    handlers.execute(event.object, event)


class SendMailField(SendBase):
    grok.implements(interfaces.ISendMailField)


@grok.subscribe(interfaces.ISendMailField)
def send_mail_field_subscriber(event):
    handlers.execute(event.object, event)
