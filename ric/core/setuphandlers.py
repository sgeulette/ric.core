# -*- coding: utf-8 -*-

from plone import api


def installCore(context):
    if context.readDataFile('ric.core-default.txt') is None:
        return

    membrane = api.portal.get_tool('membrane_tool')
    membrane.membrane_types = ['person']
