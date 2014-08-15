# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from collective.z3cform.datagridfield import DataGridField, DictRow

from ric.core import RICMessageFactory as _


class IRICPerson(model.Schema):

    form.read_permission(mailstatus='RIC: Administer website')
    form.write_permission(mailstatus='RIC: Administer website')

    mailstatus = schema.Bool(title=_(u"Statut e-mail"),
                             required=True)

    multimail = schema.List(title=_(u"Envoi mail"),
                            required=False,
                            value_type=schema.Choice(['contact cotisation',
                                                      'formation']),
                            )

alsoProvides(IRICPerson, IFormFieldProvider)


class ICotisationRow(model.Schema):

    year = schema.TextLine(title=_(u"Année"),
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
