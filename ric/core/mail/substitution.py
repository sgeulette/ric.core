# -*- coding: utf-8 -*-
from zope.component import adapts
from Products.CMFCore.interfaces import IDublinCore
from plone.stringinterp.adapters import BaseSubstitution
from ric.core import RICMessageFactory as _


class RecipientsSubstitution(BaseSubstitution):
    adapts(IDublinCore)

    category = u'RIC'
    description = _(u'Destinataires')

    def safe_call(self):
        return ', '.join(self.context.recipients)
