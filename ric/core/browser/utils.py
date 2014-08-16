# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from plone import api
from Products.Five.browser import BrowserView


class UtilsView(BrowserView):
    """
    Utils view
    """
    importantFields = []

    def isProfileCompleted(self):
        """
        Calculates profile completion depending on important fields
        and return True if content is more than 85% completed
        """
        context = self.context
        completedFields = 0
        for field in self.importantFields:
            if getattr(context, field, None) is not None:
                completedFields += 1
        completion = float(completedFields) / len(self.importantFields)
        return completion > 0.85

    def getPersonForUser(self):
        """
        Returns Person object associated to logged in user (if any)
        """
        userName = api.user.get_current().getUserName()
        membrane = api.portal.get_tool('membrane_tool')
        membraneInfos = membrane.searchResults(id=userName)
        if membraneInfos:
            return membraneInfos[0].getObject()

    def getOrganizationForUser(self):
        """
        Returns Organization object associated to Person of logged in user
        (if any)
        """
        person = self.getPersonForUser()
        if not person:
            return
        parent = aq_parent(person)
        if parent.portal_type == 'organization':
            return parent


class OrganizationView(UtilsView):
    """
    """
    importantFields = ['title',
                       'description',
                       'organization_type',
                       'phone',
                       'cell_phone',
                       'fax',
                       'email',
                       'website',
                       'number',
                       'street',
                       'zip_code',
                       'city',
                       'region',
                       'citizen',
                       'servers',
                       'softwares']


class PersonView(UtilsView):
    """
    """
    importantFields = ['lastname',
                       'firstname',
                       'birthday',
                       'phone',
                       'cell_phone',
                       'fax',
                       'email',
                       'website',
                       'number',
                       'street',
                       'zip_code',
                       'city',
                       'region']
