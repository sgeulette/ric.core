from zope.interface import Interface
from zope.component import adapts
from datetime import datetime

from plone import api
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from collective.excelexport.datasources.base import BaseContentsDataSource

EXCLUDED_TITLES = ['',
                   'Instant messenger handle',
                   'Country',
                   'Logo',
                   'Activity',
                   'Gender',
                   'Person title',
                   'Photo',
                   'Confirm Password']


class RICContentsDataSource(BaseContentsDataSource):
    """
    Export RIC contents
    """
    adapts(IPloneSiteRoot, Interface)

    def get_filename(self):
        return "RIC-%s.xls" % (datetime.now().strftime("%d-%m-%Y"))

    def get_objects(self):
        catalog = api.portal.get_tool('portal_catalog')
        query = {'portal_type': ['organization', 'person']}
        brains = catalog.searchResults(**query)
        return [b.getObject() for b in brains]

    def filter_exportables(self, exportables):
        filtered = []
        for exportable in exportables:
            if exportable.render_header() not in EXCLUDED_TITLES:
                filtered.append(exportable)
        return filtered
