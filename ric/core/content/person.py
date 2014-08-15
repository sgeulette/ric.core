# encoding: utf-8

from persistent import Persistent
from zope import schema
from zope.annotation import factory
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from collective.contact.core.content.person import Person


class IPersonCustom(Interface):

    mailstatus = schema.Bool(title=u"Statut e-mail",
                             required=True)

    multimail = schema.List(title=u"Envoi mail",
                            required=False,
                            value_type=schema.Choice(['contact cotisation',
                                                      'formation']),
                            )


class PersonExtenderFields(Persistent):
    implements(IPersonCustom)
    adapts(Person)
    mailstatus = None
    multimail = []


PersonExtenderFactory = factory(PersonExtenderFields)
