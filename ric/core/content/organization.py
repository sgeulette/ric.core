import z3c.form
from plone.directives import dexterity
from collective.contact.core.content.organization import IOrganization

from five import grok


class OrganizationEditForm(dexterity.EditForm):
    grok.context(IOrganization)
    fields = z3c.form.field.Fields(IOrganization).select('logo')
