# -*- coding: utf-8 -*-

from plone import api

from collective.contact.core.browser.organization import Organization


class OrganizationView(Organization):

    def getPersons(self):
        path = '/'.join(self.context.getPhysicalPath())
        search_path = {'query': path, 'depth': 1}
        catalog = api.portal.get_tool('portal_catalog')
        persons = catalog.searchResults(portal_type='person',
                                        sort_on='sortable_title',
                                        path=search_path)
        return persons
