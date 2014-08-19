# -*- coding: utf-8 -*-

from plone import api


def installCore(context):
    if context.readDataFile('ric.core-default.txt') is None:
        return

    membrane = api.portal.get_tool('membrane_tool')
    membrane.membrane_types = ['person']

    # Set all Authenticated Users as Member, because Membrane remove Member
    # role to Persons
    groupstool = api.portal.get_tool('portal_groups')
    groupstool.editGroup("AuthenticatedUsers", roles=["Member"], groups=())
