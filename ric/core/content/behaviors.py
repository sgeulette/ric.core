# -*- coding: utf-8 -*-

from zope import schema
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model
from collective.z3cform.datagridfield import DataGridField, DictRow
from plone import api
from zope.interface import Invalid, invariant
from z3c.form.browser.radio import RadioFieldWidget

from ric.core import RICMessageFactory as _
from ric.core.content import vocabularies


class IRICPerson(model.Schema):

    form.read_permission(invalidmail='RIC.Administrator')
    form.write_permission(invalidmail='RIC.Administrator')
    form.widget('invalidmail', RadioFieldWidget)

    invalidmail = schema.Bool(title=_(u"E-mail invalide"),
                              required=True)

    multimail = schema.List(title=_(u"Envoi mail"),
                            required=False,
                            value_type=schema.Choice(vocabulary=vocabularies.multimail),
                            )

    userid = schema.TextLine(title=_(u"Identifiant de l'utilisateur"),
                             required=False)

    @invariant
    def userid_unique(data):
        portal = api.portal.get()
        request = getattr(portal, "REQUEST", None)
        person = getMultiAdapter((portal, request),
                                 name="get_person_for_user")(data.userid)
        if person:
            raise Invalid(_(u"Utilisateur déjà existant"))


alsoProvides(IRICPerson, IFormFieldProvider)


class ICotisationRow(model.Schema):

    year = schema.Int(title=_(u"Année"),
                      required=True)

    payment = schema.Bool(title=_(u"Versement"),
                          required=True)


class IRICOrganization(model.Schema):

    form.read_permission(subscriptions='RIC: Administer website')
    form.write_permission(subscriptions='RIC: Administer website')
    form.widget('subscriptions', DataGridField)

    citizen = schema.TextLine(
        title=_(u"Nombre d'habitants"),
        required=True
    )

    servers = schema.TextLine(
        title=_(u"Serveurs"),
        required=True
    )

    softwares = schema.TextLine(
        title=_(u"Logiciels"),
        required=True
    )

    subscriptions = schema.List(
        title=_(u"Cotisations"),
        value_type=DictRow(title=_(u"Cotisation"),
                           schema=ICotisationRow),
        required=False,
    )


alsoProvides(IRICOrganization, IFormFieldProvider)
