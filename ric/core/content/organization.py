# encoding: utf-8

from persistent import Persistent
from plone.directives import form
from zope import schema
from zope.annotation import factory
from zope.component import adapts
from zope.interface import implements
from collective.z3cform.datagridfield import DictRow
from collective.contact.core.content.organization import Organization


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


class OrganizationExtenderFields(Persistent):
    implements(IOrganizationCustom)
    adapts(Organization)
    habitants = u""
    serveurs = u""
    logiciels = u""
    cotisations = []


OrganizationExtenderFactory = factory(OrganizationExtenderFields)
