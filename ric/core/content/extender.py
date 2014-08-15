# encoding: utf-8

from AccessControl import getSecurityManager
from plone import api
from plone.z3cform.fieldsets import extensible
from plone.z3cform.fieldsets.interfaces import IFormExtender
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.field import Fields
from z3c.form.interfaces import IEditForm, IAddForm, IForm
from collective.z3cform.datagridfield import DataGridFieldFactory

from ric.core.content.person import IPersonCustom
from ric.core.content.organization import IOrganizationCustom


class ContactFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, IForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        isForm = IEditForm.providedBy(self.form) or IAddForm.providedBy(self.form)
        if not isForm:
            return

        if not hasattr(self.form, 'portal_type'):
            return

        if self.form.portal_type == 'organization':
            self.remove('logo')
            self.remove('activity')
            self.add(Fields(IOrganizationCustom))
            self.form.fields['cotisations'].widgetFactory = DataGridFieldFactory
            sm = getSecurityManager()
            if not sm.checkPermission('RIC: Administer website', api.portal.get()):
                self.remove('cotisations')

        elif self.form.portal_type == 'person':
            self.remove('gender')
            self.remove('person_title')
            self.remove('photo')
            self.form.groups[0].fields['IContactDetails.email'].field.required = True
            self.add(Fields(IPersonCustom))
            sm = getSecurityManager()
            if not sm.checkPermission('RIC: Administer website', api.portal.get()):
                self.remove('mailstatus')
