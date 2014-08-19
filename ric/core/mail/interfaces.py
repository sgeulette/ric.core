# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent


class ISendNonContributor(IObjectEvent):
    pass


class ISendOrganizationMembers(IObjectEvent):
    pass


class ISendNonConnectedMembers(IObjectEvent):
    pass


class ISendMailField(IObjectEvent):
    pass
