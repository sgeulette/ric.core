# -*- encoding: utf-8 -*-

from Acquisition import aq_parent
from zope.component import adapts
from zope.component import getAdapters
from zope.interface import Interface

from collective.excelexport.exportables.dexterityfields import DexterityFieldsExportableFactory
from collective.excelexport.exportables.dexterityfields import BaseFieldRenderer

from ric.core.export.interfaces import IExtendedPersonExportable
from ric.core.export.interfaces import IExtendedOrganizationExportable


class PersonExportablesFactory(DexterityFieldsExportableFactory):
    """
    Get person extended fields
    """
    weight = 0
    portal_types = ['person']

    def get_exportables(self):
        personExtended = [ad[1] for ad in getAdapters((self.context,),
                                                      IExtendedPersonExportable)]
        return personExtended


class OrganizationExportablesFactory(DexterityFieldsExportableFactory):
    """
    Get organization extended fields
    """
    weight = 0
    portal_types = ['organization']

    def get_exportables(self):
        organizationExtended = [ad[1] for ad in getAdapters((self.context,),
                                                            IExtendedOrganizationExportable)]
        return organizationExtended


class ExtendedRenderer(BaseFieldRenderer):
    adapts(Interface)
    name = ""

    def __init__(self, context):
        self.context = context

    def __repr__(self):
        return "<%s - %s>" % (self.__class__.__name__, self.name)

    def render_header(self):
        return self.name


class RelatedOrganizationRenderer(ExtendedRenderer):
    name = "Related organization"

    def render_value(self, obj):
        parent = aq_parent(obj)
        if parent.portal_type == 'organization':
            return parent.Title()


class PathRenderer(ExtendedRenderer):
    name = "Path"

    def render_value(self, obj):
        return '/'.join(obj.getPhysicalPath())
