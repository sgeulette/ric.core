# -*- coding: utf-8 -*-
from five import grok
from zope.component.interfaces import ObjectEvent

from plone.app.contentrules import handlers

from ric.core.mail.interfaces import ISendNonContributor


class SendNonContributor(ObjectEvent):
    grok.implements(ISendNonContributor)

    def __init__(self, context, recipients):
        ObjectEvent.__init__(self, context)
        self.context = context
        self.context.recipients = recipients


@grok.subscribe(ISendNonContributor)
def send_non_contributor_subscriber(event):
    handlers.execute(event.object, event)
