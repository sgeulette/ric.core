# -*- coding: utf-8 -*-

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
                       'habitants',
                       'serveurs',
                       'logiciels']


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
