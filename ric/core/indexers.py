from plone.indexer import indexer
from Products.CMFPlone.utils import normalizeString

from collective.contact.core.content.person import IPerson


@indexer(IPerson)
def person_sortable_title(obj):
    """
    Override default sortable title to invert firstname and lastname
    """
    if obj.firstname is None:
        fullname = obj.lastname
    else:
        fullname = u"%s %s" % (obj.firstname, obj.lastname)

    return normalizeString(fullname, context=obj)
