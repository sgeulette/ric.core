import z3c.form

from AccessControl import getSecurityManager
from five import grok
from plone import api
from plone.directives import dexterity
from plone.z3cform.fieldsets import extensible
from plone.z3cform.fieldsets.interfaces import IFormExtender
from zope.component import adapts
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.contact.core.content.person import IPerson


class IPersonCustom(Interface):

    mailstatus = schema.Bool(title=u"Statut e-mail",
                             required=True)


class PersonEditForm(dexterity.EditForm):
    grok.context(IPerson)


class PersonEditFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, PersonEditForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        if not IPersonCustom.providedBy(self.context):
            alsoProvides(self.context, IPersonCustom)
        self.remove('gender')
        self.remove('person_title')
        self.remove('photo')
        self.form.groups[0].fields['IContactDetails.email'].field.required = True
        self.add(z3c.form.field.Fields(IPersonCustom))
        sm = getSecurityManager()
        if not sm.checkPermission('RIC: Administer website', api.portal.get()):
            self.remove('mailstatus')


class PersonAddForm(dexterity.AddForm):
    grok.name('person')


class PersonAddFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, PersonAddForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        if not IPersonCustom.providedBy(self.context):
            alsoProvides(self.context, IPersonCustom)
        self.remove('gender')
        self.remove('person_title')
        self.remove('photo')
        self.form.groups[0].fields['IContactDetails.email'].field.required = True
        self.add(z3c.form.field.Fields(IPersonCustom))
        sm = getSecurityManager()
        if not sm.checkPermission('RIC: Administer website', api.portal.get()):
            self.remove('mailstatus')
