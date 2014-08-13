# -*- coding: utf-8 -*-
from zope.component.interfaces import IObjectEvent


class ISendNonContributor(IObjectEvent):
    pass


class ISendCotisationPerson(IObjectEvent):
    pass


class ISendOrganisationMembers(IObjectEvent):
    pass


class ISendNonConnectedMembers(IObjectEvent):
    pass


class ISendMailField(IObjectEvent):
    pass
