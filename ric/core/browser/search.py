# -*- coding: utf-8 -*-

from plone import api
from zope.component import getMultiAdapter
from z3c.form import button, form, field
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ric.core import RICMessageFactory as _
from ric.core.browser.interfaces import IRICSearch


class RICSearchForm(form.Form):

    fields = field.Fields(IRICSearch)
    label = _(u"Recherche dans l'annuaire du RIC")
    template = ViewPageTemplateFile('templates/search.pt')
    ignoreContext = True
    _data = None
    canSearch = True
    personLink = ""

    def update(self):
        person = getMultiAdapter((self.context, self.request),
                                 name="get_person_for_user")()
        if person:
            isCompleted = getMultiAdapter((person, self.request),
                                          name="is_profile_completed")()
            if not isCompleted:
                self.personLink = person.absolute_url()
                self.canSearch = False
        super(RICSearchForm, self).update()

    @button.buttonAndHandler(_(u'Rechercher'))
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self._data = data

    def getResults(self):
        if self._data is None:
            return None
        form = self._data
        contentType = form.get('contentType')
        contentName = form.get('contentName')
        contentName = '*%s*' % contentName
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog.searchResults(portal_type=contentType,
                                       SearchableText=contentName)[:20]
        return brains

RICSearchFormView = wrap_form(RICSearchForm)
