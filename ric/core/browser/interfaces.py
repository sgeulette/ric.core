# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import TextLine, Choice

from ric.core import RICMessageFactory as _


class IRICSearch(Interface):

    contentType = Choice(title=_(u"Rechercher"),
                         vocabulary="ric.search.contents")

    contentName = TextLine(title=_(u"Nom à rechercher"),
                           required=True)
