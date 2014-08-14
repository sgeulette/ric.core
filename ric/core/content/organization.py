# encoding: utf-8
import z3c.form

from AccessControl import getSecurityManager
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.z3cform.fieldsets import extensible
from plone.z3cform.fieldsets.interfaces import IFormExtender
from zope import schema
from zope.component import adapts
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from collective.contact.core.content.organization import IOrganization
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow


class ICotisationRow(form.Schema):
    annee = schema.TextLine(title=u"Année",
                            required=True)
    versement = schema.Bool(title=u"Versement",
                            required=True)


class IOrganizationCustom(form.Schema):

    habitants = schema.TextLine(
        title=u"Nombre d'habitants",
        required=True
    )

    serveurs = schema.TextLine(
        title=u"Serveurs",
        required=True
    )

    logiciels = schema.TextLine(
        title=u"Logiciels",
        required=True
    )

    cotisations = schema.List(
        title=u"Cotisations",
        value_type=DictRow(title=u"Cotisation",
                           schema=ICotisationRow),
        required=False,
    )


class OrganizationEditForm(dexterity.EditForm):
    grok.context(IOrganization)


class OrganizationEditFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, OrganizationEditForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        loggedUser = getSecurityManager().getUser()
        userRolesForParty = loggedUser.getRoles()
        if not IOrganizationCustom.providedBy(self.context):
            alsoProvides(self.context, IOrganizationCustom)
        self.remove('logo')
        self.remove('activity')
        self.add(z3c.form.field.Fields(IOrganizationCustom))
        self.form.fields['cotisations'].widgetFactory = DataGridFieldFactory
        if 'Manager' not in userRolesForParty:
            self.remove('cotisations')


class OrganizationAddForm(dexterity.AddForm):
    grok.name('organization')


class OrganizationAddFormExtender(extensible.FormExtender):
    implements(IFormExtender)
    adapts(Interface, IDefaultBrowserLayer, OrganizationAddForm)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        loggedUser = getSecurityManager().getUser()
        userRolesForParty = loggedUser.getRoles()
        if not IOrganizationCustom.providedBy(self.context):
            alsoProvides(self.context, IOrganizationCustom)
        self.remove('logo')
        self.remove('activity')
        self.add(z3c.form.field.Fields(IOrganizationCustom))
        self.form.fields['cotisations'].widgetFactory = DataGridFieldFactory
        if 'Manager' not in userRolesForParty:
            self.remove('cotisations')
